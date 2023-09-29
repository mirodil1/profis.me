from django.urls import path

from profis.users.views import UserViewSet, WorkerListViewSet

app_name = "users"
urlpatterns = [
    path("", UserViewSet.as_view({"get": "list"}), name="list"),
    path("<int:id>/", UserViewSet.as_view({"get": "retrieve"}), name="detail"),
    path("me/", UserViewSet.as_view({"get": "me"}), name="me"),
    path("worker/all/", WorkerListViewSet.as_view({"get": "list"}), name="workers-list"),
    path(
        "worker/all/<str:category_slug>", WorkerListViewSet.as_view({"get": "list"}), name="workers-list-by-category"
    ),
]
