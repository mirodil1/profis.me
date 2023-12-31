import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from profis.categories.models import Category
from profis.core.models import TimeStampedModel
from profis.ratings.models import TaskRating
from profis.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for profis.me.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    username_validator = UnicodeUsernameValidator()

    class Gender(models.TextChoices):
        MALE = "m", _("Мужчина")
        FEMALE = "f", _("Женщина")

    _id = models.IntegerField(unique=True, db_index=True, null=True)
    first_name = models.CharField(max_length=64, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=64, verbose_name=_("Фамилия"))
    phone_number = PhoneNumberField(
        unique=True, null=True, blank=True, db_index=True, verbose_name=_("Номер телефона")
    )
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name=_("Email"))
    bio = models.TextField(null=True, blank=True, verbose_name=_("Опыт, навыки и преимущества"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Дата рождения"))
    number_of_views = models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"))
    is_worker = models.BooleanField(default=False, verbose_name=_("Статус исполнителя"))
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, verbose_name=_("Фото профиля"))
    work_experiance = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Стаж работы"))
    gender = models.CharField(choices=Gender.choices, verbose_name=_("Пол"), null=True, blank=True)
    categories = models.ManyToManyField(to=Category, related_name="user_category", verbose_name=_("Категории"))
    online_status = models.SmallIntegerField(default=0, verbose_name=_("Онлайн статус"))
    last_seen = models.DateTimeField(null=True, verbose_name=_("Последний визит"))
    username = models.CharField(
        _("username"),
        null=True,
        blank=True,
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": _("Имя пользователя уже занято."),
        },
    )

    # USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def save(self, *args, **kwargs):
        if not self._id and self.id is not None:
            self._id = 9999 + self.id
        if not self.username:
            self.username = None
        super().save(*args, **kwargs)

    @property
    def age(self):
        """
        Return age using `date_of_birth`
        """
        today = timezone.now().today()
        if self.date_of_birth:
            return (today.year - self.date_of_birth.year) - int(
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )

    @property
    def rating(self):
        """
        Getting avarage rating for the current user
        """
        avarage_score = TaskRating.objects.filter(worker=self).aggregate(Avg("score", default=0))
        return avarage_score["score__avg"]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


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
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_("Баланс"))
    status = models.CharField(max_length=6, default=Status.ACTIVE, choices=Status.choices, verbose_name=_("Статус"))

    class Meta:
        verbose_name = _("Кошелек пользователя")
        verbose_name_plural = _("Кошелек пользователя")


# class UserDocument(TimeStampedModel):
#     user = models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name="document", on_delete=models.CASCADE)
#     file = models.FileField()
#     is_business = models.BooleanField(default=False)


class PhoneNumber(TimeStampedModel):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name="phone", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True, verbose_name=_("Номер телефона"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Статус"))

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.phone_number.as_e164
