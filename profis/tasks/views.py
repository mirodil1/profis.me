from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from drf_spectacular.utils import extend_schema

from profis.tasks.models import Task, TaskImage
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
