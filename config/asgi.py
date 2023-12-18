"""
ASGI config for profis.me project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# profis directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "profis"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()
# Apply ASGI middleware here.
from config.channelsmiddleware import JWTAuthMiddleware  # noqa isort:skip

# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# Import websocket application here, so apps from django_application are loaded first
# from config.websocket import websocket_application  # noqa isort:skip
from profis.chats.routing import websocket_urlpatterns as chat_urlpatterns  # noqa isort:skip
from profis.notifications.routing import websocket_urlpatterns as notification_urlpatterns  # noqa isort:skip

websocket_urlpatterns = chat_urlpatterns + notification_urlpatterns
application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": JWTAuthMiddleware(AllowedHostsOriginValidator(URLRouter(websocket_urlpatterns))),
    }
)


# async def application(scope, receive, send):
#     if scope["type"] == "http":
#         await django_application(scope, receive, send)
#     elif scope["type"] == "websocket":
#         await websocket_application(scope, receive, send)
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")
