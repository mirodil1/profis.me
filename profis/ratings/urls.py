from django.urls import path

from profis.ratings.views import (
    OrdererTaskRatingCreateViewSet,
    OrdererTaskRatingViewSet,
    WorkerTaskRatingCreateViewSet,
    WorkerTaskRatingViewSet,
)

app_name = "ratings"

urlpatterns = [
    path("workers/all/<int:user_id>/", WorkerTaskRatingViewSet.as_view({"get": "list"}, name="workers-ratings-list")),
    path(
        "orderers/all/<int:user_id>/", OrdererTaskRatingViewSet.as_view({"get": "list"}, name="orderers-ratings-list")
    ),
    path("workers/rate/", WorkerTaskRatingCreateViewSet.as_view({"post": "create"}, name="workers-ratings-create")),
    path("orderers/rate/", OrdererTaskRatingCreateViewSet.as_view({"post": "create"}, name="orderers-ratings-create")),
]
