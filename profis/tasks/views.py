from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from profis.tasks.models import Task
from profis.tasks.permissions import IsWorker
from profis.tasks.serializers import TaskCreateSerializer, TaskSerializer


@extend_schema(tags=["tasks"])
class TaskListRetrieveViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "id"


@extend_schema(tags=["tasks"])
class TaskCreateViewSet(CreateModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsWorker, IsAuthenticated]
