from django.urls import path

from profis.notifications.views import NotificationListViewSet

app_name = "notifications"
urlpatterns = [
    path("all/", NotificationListViewSet.as_view({"get": "list"}), name="list"),
]
