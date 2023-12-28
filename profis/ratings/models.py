from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from profis.core.models import TimeStampedModel
from profis.tasks.models import Task


class TaskRating(TimeStampedModel):
    worker = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="ratings_received",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Исполнитель"),
    )
    orderer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="ratings_given",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Заказчик"),
    )
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, verbose_name=_("Задание"))
    score = models.PositiveSmallIntegerField(default=0, verbose_name=_("Балл"))
    review = models.TextField(verbose_name=_("Отзыв"))

    class Meta:
        verbose_name = _("Рейтинг")
        verbose_name_plural = _("Рейтинги")
        constraints = [
            models.UniqueConstraint(fields=["worker", "task"], name="unique_worker_rating"),
            models.UniqueConstraint(fields=["orderer", "task"], name="unique_orderer_rating"),
        ]

    def __str__(self) -> str:
        return f"{self.orderer.first_name} -> {self.worker.first_name}: {self.score} stars"
