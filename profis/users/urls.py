from django.urls import path

from profis.users.views import UserViewSet

app_name = "users"
urlpatterns = [
    path("", UserViewSet.as_view({"get": "list"}), name="list"),
    path("<int:id>/", UserViewSet.as_view({"get": "retrieve"}), name="detail"),
    path("me/", UserViewSet.as_view({"get": "me"}), name="me"),
]
