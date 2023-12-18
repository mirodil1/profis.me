from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "profis.notifications"
    verbose_name = _("Нотификации")

    def ready(self):
        try:
            import profis.notifications.signals  # noqa: F401
        except ImportError:
            pass
