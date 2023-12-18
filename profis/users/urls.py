from django.urls import path

from profis.users.views import UserRedirectView, UserViewSet, WorkerListViewSet

app_name = "users"

urlpatterns = [
    # Users urls
    path("", UserViewSet.as_view({"get": "list"}), name="list"),
    path("<int:id>/", UserViewSet.as_view({"get": "retrieve"}), name="detail"),
    path("me/", UserViewSet.as_view({"get": "me"}), name="me"),
    # Workers urls
    path("worker/all/", WorkerListViewSet.as_view({"get": "list"}), name="workers-list"),
    path(
        "worker/all/<str:category_slug>/", WorkerListViewSet.as_view({"get": "list"}), name="workers-list-by-category"
    ),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
]
