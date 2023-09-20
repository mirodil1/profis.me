from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "profis.users"
    verbose_name = _("Пользователи")

    def ready(self):
        try:
            import profis.users.signals  # noqa: F401
        except ImportError:
            pass
