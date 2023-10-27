from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from profis.categories.models import Category
from profis.core.models import TimeStampedModel


class UserPlan(TimeStampedModel):
    class PlanType(models.TextChoices):
        UNLIM = "unlim", _("Безлимитный")
        BASE = "base", _("Базовый")

    class PackageType(models.TextChoices):
        UNLIM_15 = "unlim_15", _("Безлимитный 15")
        UNLIM_30 = "unlim_30", _("Безлимитный 30")
        UNLIM_90 = "unlim_90", _("Безлимитный 90")
        BASE_25 = "base_25", _("Базовый 25")
        BASE_50 = "base_50", _("Базовый 50")
        BASE_100 = "base_100", _("Базовый 100")

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Пользовател"))
    categories = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=_("Категории"))
    expired_at = models.DateTimeField(verbose_name=_("Срок действия"))
    plan_type = models.CharField(choices=PlanType.choices, verbose_name=_("Тип тарифа"))
    package_type = models.CharField(choices=PackageType.choices, verbose_name=_("Тип пакета"))
    number_of_responses = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name=_("Количество откликов")
    )

    class Meta:
        verbose_name = _("План пользователей")
        verbose_name_plural = _("Планы пользователей")

    def __str__(self) -> str:
        return f"{self.user.first_name} - {self.plan_type}"

    def save(self, *args, **kwargs):
        if not self.expired_at:
            if self.plan_type == self.PlanType.BASE:
                self.expired_at = timezone.now() + timedelta(days=30)

            elif self.plan_type == self.PlanType.UNLIM:
                if self.package_type == self.PackageType.UNLIM_15:
                    self.expired_at = timezone.now() + timedelta(days=15)
                elif self.package_type == self.PackageType.UNLIM_30:
                    self.expired_at = timezone.now() + timedelta(days=30)
                elif self.package_type == self.PackageType.UNLIM_90:
                    self.expired_at = timezone.now() + timedelta(days=90)
        return super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.expired_at > timezone.now()
