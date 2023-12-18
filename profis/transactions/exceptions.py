from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException


class BasePaymeException(APIException):
    """
    BasePaymeException
    """

    status_code = 200
    error_code = None
    message = None

    # pylint: disable=super-init-not-called
    def __init__(self, error_message: str = None):
        detail: dict = {"error": {"code": self.error_code, "message": self.message, "data": error_message}}
        self.detail = detail


class PermissionDenied(BasePaymeException):
    """
    PermissionDenied APIException that is raised when the client is not allowed to server.
    """

    status_code = 200
    error_code = -32504
    message = _("Недостаточно привилегий для выполнения метода")


class MethodNotFound(BasePaymeException):
    """
    MethodNotFound APIException that is raised when the method does not exist.
    """

    status_code = 405
    error_code = -32601
    message = _("Запрашиваемый метод не найден")


class TooManyRequests(BasePaymeException):
    """
    TooManyRequests APIException that is raised when the request exceeds the limit.
    """

    status_code = 200
    error_code = -31099
    message = {
        "uz": "Buyurtma tolovni amalga oshirish jarayonida",
        "ru": "Транзакция в очереди",
        "en": "Order payment status is queued",
    }


class IncorrectAmount(BasePaymeException):
    """
    IncorrectAmount APIException that is raised when the amount is not incorrect.
    """

    status_code = 200
    error_code = -31001
    message = {
        "uz": "Noto'g'ri miqdor",
        "ru": "Неверная сумма",
        "en": "Incorrect amount",
    }


class PerformTransactionDoesNotExist(BasePaymeException):
    """
    PerformTransactionDoesNotExist APIException that is raised when a transaction does not exist or deleted.
    """

    status_code = 200
    error_code = -31050
    message = {
        "uz": "Foydalanuvchi topilmadi",
        "ru": "Пользователь не найден",
        "en": "User not found",
    }


class TransactionDoesNotExist(BasePaymeException):
    """
    TransactionDoesNotExist APIException that is raised when a transaction not found.
    """

    status_code = 200
    error_code = -31003
    message = {
        "uz": "Tranzaksiya topilmadi",
        "ru": "Транзакция не найдена",
        "en": "Transaction not found",
    }


class OrderCompleted(BasePaymeException):
    """
    TransactionDoesNotExist APIException that is raised when a transaction not found.
    """

    status_code = 200
    error_code = -31007
    message = {
        "uz": "Buyurtma bajarildi. Bitimni bekor qilish mumkin emas. \
               Tovar yoki xizmat xaridorga to'liq hajmda taqdim etilgan",
        "ru": "Заказ выполнен. Невозможно отменить транзакцию. \
               Товар или услуга предоставлена покупателю в полном объеме",
        "en": "The order is completed. It is not possible to cancel the transaction. \
               The product or service is provided to the buyer in full",
    }


class TransactionStateDisallowed(BasePaymeException):
    """
    TransactionDoesNotExist APIException that is raised when the state of the transaction does not
    allow the operation to be performed.
    """

    status_code = 200
    error_code = -31008
    message = {
        "uz": "Operatsiyani bajarish mumkin emas",
        "ru": "Невозможно выполнить операцию",
        "en": "The operation cannot be performed",
    }


class PaymeTimeoutException(Exception):
    """
    Payme timeout exception that means that payme is working slowly.
    """
