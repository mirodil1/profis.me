from django.urls import path

from profis.chats.views import ChatCreateViewSet, MessageCreateViewSet

app_name = "chats"

urlpatterns = [
    path("new/", ChatCreateViewSet.as_view({"post": "create"}), name="create"),
    path("message/upload/", MessageCreateViewSet.as_view({"post": "create"}), name="message-create"),
]
