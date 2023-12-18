from django.apps import AppConfig


class MessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "profis.chats"

    def ready(self):
        try:
            import profis.chats.signals  # noqa: F401
        except ImportError:
            pass
