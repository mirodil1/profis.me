from django.urls import path

from profis.tasks.views import TaskCreateViewSet, TaskListRetrieveViewSet

app_name = "tasks"

urlpatterns = [
    path("", TaskListRetrieveViewSet.as_view({"get": "list"}), name="list"),
    path("<int:id>/", TaskListRetrieveViewSet.as_view({"get": "retrieve"}), name="detail"),
    path("new/", TaskCreateViewSet.as_view({"post": "create"}), name="create"),
]
