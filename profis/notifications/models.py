from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from profis.core.models import TimeStampedModel


class Notification(TimeStampedModel):
    """
    Notification model
    """

    class NotificationType(models.TextChoices):
        MESSAGE = "message", _("Message")
        RESPONSE = "response", _("Response")
        BROADCAST = "broadcast", _("Broadcast")
        FEEDBACK = "feedback", _("Feedback")
        TRANSACTION = "transaction", _("Transaction")
        SUBSCRIBTION = "subscribtion", _("Subscribtion")

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    message = models.TextField(verbose_name=_("Текст"))
    notification_type = models.CharField(
        choices=NotificationType.choices, default=NotificationType.BROADCAST, verbose_name=_("Тип нотификации")
    )
    is_read = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name = _("Нотификации")
        verbose_name_plural = _("Нотификации")

    def __str__(self) -> str:
        return f"{self.notification_type} to {self.user}"
