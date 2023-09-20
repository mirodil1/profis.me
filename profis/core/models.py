from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Abstract Timestamp model
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Созданное время"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновленное время"))

    class Meta:
        abstract = True
