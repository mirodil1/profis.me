import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from profis.categories.models import Category
from profis.core.models import TimeStampedModel
from profis.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for profis.me.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    class Gender(models.TextChoices):
        MALE = "m", _("Мужчина")
        FEMALE = "f", _("Женщина")

    first_name = models.CharField(max_length=64, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=64, verbose_name=_("Фамилия"))
    phone_number = PhoneNumberField(unique=True, null=True, blank=True, verbose_name=_("Номер телефона"))
    email = models.EmailField(_("Email"), unique=True)
    bio = models.TextField(null=True, blank=True, verbose_name=_("Опыт, навыки и преимущества"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Дата рождения"))
    number_of_views = models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"))
    is_worker = models.BooleanField(default=False, verbose_name=_("Статус исполнителя"))
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, verbose_name=_("Фото профиля"))
    work_experiance = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Стаж работы"))
    gender = models.CharField(choices=Gender.choices, verbose_name=_("Пол"), null=True, blank=True)
    categories = models.ManyToManyField(
        to=Category, related_name="user_category", null=True, blank=True, verbose_name=_("Категории")
    )
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    @property
    def age(self):
        """
        Return the age using `date_of_birth`
        """
        today = timezone.now().today()
        if self.date_of_birth:
            return (today.year - self.date_of_birth.year) - int(
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )

    def __str__(self) -> str:
        return self.email


class UserWallet(TimeStampedModel):
    class Status(models.TextChoices):
        """
        Status of the wallet
        """

        ACTIVE = "active", _("Активный")
        FROZEN = "frozen", _("Замароженный")
        CLOSED = "closed", _("Закрытый")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name=_("ID"))
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    balance = models.PositiveIntegerField(default=0, verbose_name=_("Баланс"))
    status = models.CharField(max_length=6, default=Status.ACTIVE, choices=Status.choices, verbose_name=_("Статус"))

    class Meta:
        verbose_name = _("Кошелек пользователя")
        verbose_name_plural = _("Кошелек пользователя")
