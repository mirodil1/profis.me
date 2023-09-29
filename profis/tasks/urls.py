from django.urls import path

from profis.tasks.views import (
    CurrentUserTaskListViewSet,
    CurrentUserTaskResponseListViewSet,
    TaskCreateViewSet,
    TaskListRetrieveViewSet,
    TaskResponseCraeteViewSet,
    TaskResponseListViewSet,
    TaskResponseWorkerAPIView,
)

app_name = "tasks"

urlpatterns = [
    # Task
    path("all/", TaskListRetrieveViewSet.as_view({"get": "list"}), name="task-list"),
    path("<int:id>/", TaskListRetrieveViewSet.as_view({"get": "retrieve"}), name="task-detail"),
    path("new/", TaskCreateViewSet.as_view({"post": "create"}), name="task-create"),
    path("update/<int:id>/", TaskCreateViewSet.as_view({"put": "update"}), name="task-update"),
    # Task response
    path("responses/<int:task_id>/", TaskResponseListViewSet.as_view({"get": "list"}), name="response-list-by-task"),
    path(
        "responses/new-respond/",
        TaskResponseCraeteViewSet.as_view({"post": "create"}),
        name="task-response-create",
    ),
    path(
        "response/select/<int:worker_id>/<int:task_id>/",
        TaskResponseWorkerAPIView.as_view(),
        name="resopnse-accept-worker",
    ),
    # User tasks
    path("my-tasks/", CurrentUserTaskListViewSet.as_view({"get": "list"}), name="user-task-list"),
    path("my-responses/", CurrentUserTaskResponseListViewSet.as_view({"get": "list"}), name="user-response-list"),
]
