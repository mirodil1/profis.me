from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "profis.tasks"
    verbose_name = _("Задания")

    def ready(self):
        try:
            import profis.tasks.signals  # noqa: F401
        except ImportError:
            pass
