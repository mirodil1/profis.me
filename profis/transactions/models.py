from django.db import models
from django.utils.translation import gettext_lazy as _

from profis.core.models import TimeStampedModel


class Transaction(TimeStampedModel):
    class TransactionStatus(models.TextChoices):
        PPROCESSING = "processing", _("В процессе")
        SUCCESS = "success", _("Успешно")
        FAILED = "failed", _("Ошибка")
        CANCELED = "canceled", _("Отменено")

    _id = models.CharField(max_length=255, db_index=True, verbose_name=_("ID Транзакции"))
    user_id = models.IntegerField(null=True, db_index=True, verbose_name=_("ID Пользователя"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Сумма"))
    state = models.IntegerField(blank=True, null=True, default=1, verbose_name=_("6"))
    status = models.CharField(choices=TransactionStatus.choices, max_length=55, verbose_name=_("Статус транзакции"))
    create_time = models.BigIntegerField(null=True)
    perform_time = models.BigIntegerField(null=True)
    cancel_time = models.BigIntegerField(null=True)
    reason = models.IntegerField(null=True)

    class Meta:
        verbose_name = _("Транзакция")
        verbose_name_plural = _("Транзакции")

    def __str__(self) -> str:
        return self._id
