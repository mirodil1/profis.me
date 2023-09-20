from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
    email = models.EmailField(_("Email"), unique=True)
    username = None
    bio = models.TextField(null=True, blank=True, verbose_name=_("Опыт, навыки и преимущества"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Дата рождения"))
    number_of_views = models.PositiveIntegerField(default=0, verbose_name=_("Просмотры"))
    is_worker = models.BooleanField(default=False, verbose_name=_("Статус исполнителя"))
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, verbose_name=_("Фото профиля"))
    work_experiance = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Стаж работы"))
    gender = models.CharField(choices=Gender.choices, verbose_name=_("Пол"), null=True, blank=True)

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

        return (today.year - self.date_of_birth.year) - int(
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
