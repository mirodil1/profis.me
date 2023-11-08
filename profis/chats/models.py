from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from profis.core.models import TimeStampedModel


class Chat(TimeStampedModel):
    chat_name = models.CharField(max_length=64, unique=True, verbose_name=_("ads"))
    participants = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="chats")

    def __str__(self) -> str:
        return self.chat_name


class Message(TimeStampedModel):
    participants = models.ForeignKey(
        to=Chat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chats",
    )
    sender = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Отправитель")
    )
    content = models.TextField(null=True, blank=True, verbose_name=_("Контент"))
    file = models.FileField(
        upload_to="files",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(["pdf", "jpeg", "jpg", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"])
        ],
        verbose_name=_("Файл"),
    )
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.sender}"
