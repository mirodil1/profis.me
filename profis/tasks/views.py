from typing import Any

from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from profis.subscription.models import UserPlan
from profis.tasks.models import Task, TaskResponse
from profis.tasks.permissions import IsWorker
from profis.tasks.serializers import (
    TaskCreateSerializer,
    TaskResponseCreateSerializer,
    TaskResponseSerializer,
    TaskSerializer,
)


@extend_schema(tags=["tasks"])
class TaskListRetrieveViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "id"

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(status=Task.Status.OPEN)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()

        # Update the number_of_views attribute by incrementing it
        instance.number_of_views += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=["tasks"])
class TaskCreateViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["task-responses"])
class TaskResponseListViewSet(ListModelMixin, GenericViewSet):
    queryset = TaskResponse.objects.all()
    serializer_class = TaskResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        task_id = self.kwargs.get("task_id")
        qs = qs.filter(task__owner=self.request.user, task__id=task_id)

        return qs


@extend_schema(tags=["task-responses"])
class TaskResponseCraeteViewSet(CreateModelMixin, GenericViewSet):
    queryset = TaskResponse.objects.all().select_related()
    serializer_class = TaskResponseCreateSerializer
    permission_classes = [IsWorker, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get the user making the request
            user = request.user
            # Get the task for which the response is being created
            task = serializer.validated_data["task"]

            response_type = serializer.validated_data["response_type"]
            if response_type == TaskResponse.ResponseType.PLAIN:
                # Get category price
                price = task.category.price

                user.userwallet.balance = F("balance") - price
                user.userwallet.save()
            # elif response_type == TaskResponse.ResponseType.POST:
            #     pass
            elif response_type == TaskResponse.ResponseType.BASE:
                plan = user.userplan_set.get(
                    plan_type=UserPlan.PlanType.BASE,
                    expired_at__gt=timezone.now(),
                    categories=task.category.parent_category,
                )
                if plan.number_of_responses > 0:
                    plan.number_of_responses = F("number_of_responses") - 1
                    plan.save()
                else:
                    response = {"error": "Нет откликов"}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            # elif response_type == TaskResponse.ResponseType.UNLIM:
            #     pass

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=["user-tasks"])
class CurrentUserTaskListViewSet(ListModelMixin, GenericViewSet):
    """
    Return tasks related to current user
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        return qs.filter(owner=user)


@extend_schema(tags=["user-tasks"])
class CurrentUserTaskResponseListViewSet(ListModelMixin, GenericViewSet):
    """
    Return responses related to current user
    """

    queryset = TaskResponse.objects.all()
    serializer_class = TaskResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(worker=self.request.user)


@extend_schema(tags=["task-responses"])
class TaskResponseWorkerAPIView(APIView):
    """
    Choose worker for the task
    """

    def get(self, request, worker_id, task_id):
        task = get_object_or_404(Task, id=task_id)
        task_response = get_object_or_404(TaskResponse, task=task, worker_id=worker_id)
        if not task.worker:
            try:
                # Update TaskResponse status
                task_response.status = TaskResponse.STATUS.ACCEPTED
                task_response.save()

                # Update Task worker and status
                task.worker_id = worker_id
                task.status = Task.Status.IN_PROGRESS
                task.save()

                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Task already has a worker
            return Response({"error": _("У задачи уже есть исполнитель.")}, status=status.HTTP_400_BAD_REQUEST)
