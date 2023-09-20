from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from profis.categories.models import Category
from profis.core.models import TimeStampedModel


class Task(TimeStampedModel):
    """
    Task model
    """

    class Status(models.TextChoices):
        OPEN = "open", _("Открыто")
        CLOSED = "closed", _("Закрыто")

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=_("Категория"))
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    name = models.CharField(max_length=255, verbose_name=_("Название задание"))
    description = models.TextField(verbose_name=_("Подробное описание"))
    phone_number = models.CharField(max_length=15, verbose_name=_("Номер телефона"))
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.CLOSED)
    start_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Время начала"))
    finish_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Время окончания"))
    file = models.FileField(null=True, blank=True, verbose_name=_("Файл"))
    number_of_views = models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"))

    class Meta:
        verbose_name = _("Задание")
        verbose_name_plural = _("Задания")

    def __str__(self) -> str:
        return self.name


class TaskImage(TimeStampedModel):
    """
    Image model for tasks
    """

    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, related_name="images", verbose_name=_("Задание"))
    image = models.ImageField(upload_to="tasks", verbose_name=_("Фото"))
