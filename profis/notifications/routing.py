from django.urls import path

from profis.notifications.consumers import ChatNotificationConsumer, NotificationConsumer

websocket_urlpatterns = [
    path("ws/notification/", NotificationConsumer.as_asgi()),
    path("ws/chat/notification/", ChatNotificationConsumer.as_asgi()),
]
