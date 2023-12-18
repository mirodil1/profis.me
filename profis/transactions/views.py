import base64
import binascii
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.utils.translation import gettext as _
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from profis.transactions.exceptions import (
    IncorrectAmount,
    MethodNotFound,
    OrderCompleted,
    PerformTransactionDoesNotExist,
    PermissionDenied,
    TransactionDoesNotExist,
    TransactionStateDisallowed,
)
from profis.transactions.models import Transaction
from profis.transactions.serializers import TransactionSerializer

User = get_user_model()


class TransactionAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        password = request.headers.get("authorization")

        if self.authorize(password):
            data = request.data
            method = data.get("method")

            if method == "CheckPerformTransaction":
                response = self.check_perform_transaction(data)
            elif method == "CreateTransaction":
                response = self.create_transaction(data)
            elif method == "PerformTransaction":
                response = self.perform_transaction(data)
            elif method == "CancelTransaction":
                response = self.cancel_transaction(data)
            elif method == "CheckTransaction":
                response = self.check_transaction(data)
            elif method == "GetStatement":
                response = self.get_statement(data)
            else:
                raise MethodNotFound()
        else:
            raise PermissionDenied()

        return Response(response)

    def check_perform_transaction(self, data):
        """
        Check perform transaction, if payment is possible then return `allow=True`
        """
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Get validated data
        params = serializer.validated_data.get("params")
        amount = params.get("amount")
        user_id = params.get("account").get("user_id")

        if amount >= settings.PAYME_MIN_AMOUNT and User.objects.filter(_id=user_id).exists():
            response = {
                "result": {
                    "allow": True,
                }
            }
        elif amount < settings.PAYME_MIN_AMOUNT:
            raise IncorrectAmount()
        else:
            raise PerformTransactionDoesNotExist()

        return response

    def create_transaction(self, data):
        """
        Create transaction
        """
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Get validated data
        params = serializer.validated_data.get("params")
        user_id = params.get("account").get("user_id")
        transaction_id = params.get("id")
        amount = params.get("amount")

        if amount <= settings.PAYME_MIN_AMOUNT:
            raise IncorrectAmount()
        if not User.objects.filter(_id=user_id).exists():
            raise PerformTransactionDoesNotExist()

        transaction = Transaction.objects.filter(_id=transaction_id).last()
        if transaction is not None:
            if transaction.state == 1:
                # Check for `timeout`
                if int(time.time() * 1000) - transaction.create_time > 43200000:
                    transaction.state = -1
                    transaction.reason = 4
                    transaction.save()
                    raise TransactionStateDisallowed()
                else:
                    response = {
                        "result": {
                            "create_time": int(transaction.create_time),
                            "transaction": transaction._id,
                            "state": int(transaction.state),
                        }
                    }
            else:
                raise TransactionStateDisallowed()
        else:
            transaction, _ = Transaction.objects.get_or_create(
                _id=transaction_id,
                user_id=user_id,
                amount=amount / 100,
                status=Transaction.TransactionStatus.PPROCESSING,
                create_time=int(time.time() * 1000),
            )
            if transaction:
                response = {
                    "result": {
                        "create_time": int(transaction.create_time),
                        "transaction": transaction._id,
                        "state": int(transaction.state),
                    }
                }

        return response

    def perform_transaction(self, data):
        """
        The PerformTransaction method deposits funds to the merchant's account
          and sets the status of the order to `success`
        """
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        clean_data = serializer.validated_data
        params = clean_data.get("params")

        try:
            transaction = Transaction.objects.get(
                _id=params.get("id"),
            )
            if transaction.state == 1:
                if int(time.time() * 1000) - transaction.create_time < 43200000:
                    transaction.state = 2
                    transaction.status = Transaction.TransactionStatus.SUCCESS
                    if not transaction.perform_time:
                        transaction.perform_time = int(time.time() * 1000)
                    transaction.save()

                    # Get user and fill the balance
                    user = User.objects.get(_id=transaction.user_id)
                    user.userwallet.balance += transaction.amount
                    user.userwallet.save()

                    response = {
                        "result": {
                            "perform_time": int(transaction.perform_time),
                            "transaction": transaction._id,
                            "state": int(transaction.state),
                        }
                    }
                else:
                    # Cancel transaction
                    transaction.state = -1
                    transaction.reason = 4
                    transaction.save()
                    raise TransactionStateDisallowed()
            else:
                if transaction.state == 2:
                    response = {
                        "result": {
                            "perform_time": int(transaction.perform_time),
                            "transaction": transaction._id,
                            "state": int(transaction.state),
                        }
                    }
                else:
                    raise TransactionStateDisallowed()
        except User.DoesNotExist:
            raise PerformTransactionDoesNotExist()
        except Transaction.DoesNotExist:
            raise TransactionDoesNotExist()

        return response

    def check_transaction(self, data):
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        clean_data = serializer.validated_data
        params = clean_data.get("params")
        try:
            transaction = Transaction.objects.get(
                _id=params.get("id"),
            )
            response = {
                "result": {
                    "create_time": transaction.create_time,
                    "perform_time": 0 if not transaction.perform_time else transaction.perform_time,
                    "cancel_time": 0 if not transaction.cancel_time else transaction.cancel_time,
                    "transaction": transaction._id,
                    "state": transaction.state,
                    "reason": None,
                }
            }
            if transaction.reason is not None:
                response["result"]["reason"] = int(transaction.reason)

        except Transaction.DoesNotExist as error:
            raise TransactionDoesNotExist() from error

        return response

    def cancel_transaction(self, data):
        """
        The CancelTransaction method cancels both the created and completed transaction
        """
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        clean_data = serializer.validated_data
        params = clean_data.get("params")
        try:
            transaction = Transaction.objects.get(_id=params.get("id"))
            user = User.objects.get(_id=transaction.user_id)

            if transaction.state == 1:
                transaction.state = -1
            if transaction.state == 2:
                if user.userwallet.balance >= transaction.amount:
                    transaction.state = -2

                    # Cancel payment from user balance
                    user.userwallet.balance -= transaction.amount
                    user.userwallet.save()
                else:
                    raise OrderCompleted()
            if transaction.cancel_time is None:
                transaction.cancel_time = int(time.time() * 1000)
            transaction.status = Transaction.TransactionStatus.CANCELED
            transaction.reason = params.get("reason")
            transaction.save()
        except User.DoesNotExist:
            raise PerformTransactionDoesNotExist()
        except Transaction.DoesNotExist:
            raise TransactionDoesNotExist()

        response: dict = {
            "result": {
                "state": transaction.state,
                "cancel_time": transaction.cancel_time,
                "transaction": transaction._id,
                "reason": int(transaction.reason),
            }
        }

        return response

    def get_statement(self, data):
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        clean_data = serializer.validated_data
        params = clean_data.get("params")
        try:
            transactions = Transaction.objects.filter(
                create_time__gte=params.get("from"), create_time__lte=params.get("to")
            )

            if not transactions:  # no transactions found for the period
                return {"result": {"transactions": []}}

            statements = [
                {
                    "id": t._id,
                    "time": int(t.created_at.timestamp()),
                    "amount": t.amount,
                    "account": {"user_id": t.user_id},
                    "create_time": t.create_time,
                    "perform_time": 0 if not t.perform_time else t.perform_time,
                    "cancel_time": 0 if not t.cancel_time else t.cancel_time,
                    "transaction": t._id,
                    "state": t.state,
                    "reason": t.reason,
                    "receivers": [],  # not implemented
                }
                for t in transactions
            ]

            response: dict = {"result": {"transactions": statements}}
        except DatabaseError:
            response = {"result": {"transactions": []}}

        return response

    @staticmethod
    def authorize(password):
        """
        Authorize the Merchant.
        :param password: string -> Merchant authorization password
        """
        is_payme = False
        error_message = ""

        if not isinstance(password, str):
            error_message = "Request from an unauthorized source!"
            raise PermissionDenied(error_message=error_message)
        password = password.split()[-1]
        try:
            password = base64.b64decode(password).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError) as error:
            error_message = _("Недостаточно привилегий для выполнения метода")
            raise PermissionDenied(error_message=error_message) from error

        merchant_key = password.split(":")[-1]
        if merchant_key == settings.PAYME_KEY:
            is_payme = True

        if merchant_key != settings.PAYME_KEY:
            raise PermissionDenied(error_message="Unavailable data for unauthorized users!")

        return is_payme
