from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from profis.notifications.models import Notification
from profis.notifications.serializers import NotificationSerializer


@extend_schema(tags=["notifications"])
class NotificationListViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return (
            qs.filter(user=self.request.user)
            .exclude(notification_type=Notification.NotificationType.MESSAGE)
            .order_by("-created_at")
        )
