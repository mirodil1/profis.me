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
        IN_PROGRESS = "in_progress", _("Выполняется")
        COMPLETED = "completed", _("Выполнено")
        NOT_COMPLETED = "not_completed", _("Не выполнено")
        CLOSED = "closed", _("Закрыто")

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=_("Категория"))
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="owner_task",
        on_delete=models.CASCADE,
        verbose_name=_("Заказчик"),
    )
    worker = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="worker_task",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Исполнитель"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Название задание"))
    description = models.TextField(verbose_name=_("Подробное описание"))
    budget = models.PositiveIntegerField(default=0, verbose_name=_("Бюджет"))
    phone_number = models.CharField(max_length=15, verbose_name=_("Номер телефона"))
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)
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

    class Meta:
        verbose_name = _("Фото")
        verbose_name_plural = _("Фото")

    def __str__(self) -> str:
        return self.task.name


class TaskAddress(TimeStampedModel):
    """
    Address model for tasks
    """

    class Point(models.TextChoices):
        A = "a", _("А")
        B = "b", _("Б")
        V = "v", _("В")
        G = "g", _("Г")
        D = "d", _("Д")
        E = "e", _("Е")
        J = "j", _("Ж")
        Z = "z", _("З")
        Q = "i", _("И")
        K = "k", _("К")
        L = "l", _("Л")

    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, related_name="address", verbose_name=_("Задание"))
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    point = models.CharField(choices=Point.choices, default=Point.A, verbose_name=_("Точка"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["task", "point"], name="unique_task_point"),
        ]
        verbose_name = _("Адрес")
        verbose_name_plural = _("Адреса")

    def __str__(self) -> str:
        return self.name


class TaskResponse(TimeStampedModel):
    class STATUS(models.TextChoices):
        PENDING = "pending", _("Рассматриваемый")
        ACCEPTED = "accepted", _("Принято")

    class ResponseType(models.TextChoices):
        PLAIN = "plain", _("Обычный")
        BASE = "base", _("Базовый")
        UNLIM = "unlim", _("Безлимитный")
        POST = "post", _("Постоплата")

    task = models.ForeignKey(to=Task, related_name="responses", on_delete=models.CASCADE, verbose_name=_("Задание"))
    worker = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Исполнитель"))
    price = models.PositiveIntegerField(default=0, verbose_name=_("Цена"))
    text = models.TextField(verbose_name=_("Текст"))
    status = models.CharField(max_length=12, choices=STATUS.choices, default=STATUS.PENDING, verbose_name=_("СТАТУС"))
    response_type = models.CharField(choices=ResponseType.choices, verbose_name=_("Тип отклика"))

    def __str__(self):
        return f"Response to '{self.task.name}' by {self.worker.first_name}"

    class Meta:
        verbose_name = _("Отклик")
        verbose_name_plural = _("Отклик")
