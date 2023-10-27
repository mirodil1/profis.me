from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from profis.subscription.models import UserPlan
from profis.subscription.serializers import UserPlanCreateSerializer, UserPlanSerializer


class UserPlanListViewSet(ListModelMixin, GenericViewSet):
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanSerializer


class UserPlanCreateViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # getting `total_amount` and `user`
            total_amount = serializer.validated_data.get("total_amount")
            user = serializer.validated_data.get("user")

            # subtract total amount from user balance
            user_wallet = user.userwallet
            user_wallet.balance -= total_amount
            user_wallet.save()

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED, headers=headers)
