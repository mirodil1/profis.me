from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscriptionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "profis.subscription"
    verbose_name = _("Тарифы")
