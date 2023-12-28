from django.urls import path

from profis.ratings.views import TaskRatingCreateViewSet, TaskRatingViewSet

app_name = "ratings"

urlpatterns = [
    path("workers/all/<int:user_id>/", TaskRatingViewSet.as_view({"get": "list"}, name="workers-rating-list")),
    path("workers/rate/", TaskRatingCreateViewSet.as_view({"post": "create"}, name="workers-rating-create")),
]
