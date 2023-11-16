from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError

from profis.ratings.models import TaskRating
from profis.tasks.models import Task


class WorkerTaskRatingSerializer(serializers.ModelSerializer):
    worker = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    class Meta:
        model = TaskRating
        fields = [
            "worker",
            "task",
            "review",
            "score",
        ]

    def get_worker(self, obj):
        worker = obj.task.worker
        return {"id": worker.id, "first_name": worker.first_name, "last_name": worker.last_name}

    def get_task(self, obj):
        task = obj.task
        return {"id": task.id, "name": task.name}


class OrdererTaskRatingSerializer(serializers.ModelSerializer):
    orderer = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    class Meta:
        model = TaskRating
        fields = [
            "orderer",
            "task",
            "score",
            "review",
            "created_at",
        ]

    def get_orderer(self, obj):
        orderer = obj.task.owner
        return {"id": orderer.id, "first_name": orderer.first_name, "last_name": orderer.last_name}

    def get_task(self, obj):
        task = obj.task
        return {"id": task.id, "name": task.name}


class WorkerTaskRatingCreateSerializer(serializers.ModelSerializer):
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True)

    class Meta:
        model = TaskRating
        validators = [
            validators.UniqueTogetherValidator(
                queryset=TaskRating.objects.all(),
                fields=["worker", "task"],
                message=_("Рейтинг с той же задачей и исполнителем уже существует"),
            )
        ]
        fields = [
            "worker",
            "task",
            "score",
            "review",
        ]

    def validate(self, validated_data):
        worker = validated_data.get("worker")
        task = validated_data.get("task")

        # Check if the worker is the same as the orderer (owner of the task)
        if worker == task.owner:
            raise ValidationError(_("Вы не можете оценивать себя как исполнителя"))

        # Check if the worker is related to this task
        if worker != task.worker:
            raise ValidationError(_("вы не являетесь исполнителем этой заданий"))

        return validated_data


class OrdererTaskRatingCreateSerializer(serializers.ModelSerializer):
    orderer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True)

    class Meta:
        model = TaskRating
        validators = [
            validators.UniqueTogetherValidator(
                queryset=TaskRating.objects.all(),
                fields=["orderer", "task"],
                message=_("Рейтинг с той же задачей и заказчиком уже существует"),
            )
        ]
        fields = [
            "orderer",
            "task",
            "score",
            "review",
        ]

    def validate(self, validated_data):
        orderer = validated_data.get("orderer")
        task = validated_data.get("task")

        # Check if the worker is the same as the orderer (owner of the task)
        if orderer != task.owner:
            raise ValidationError(_("Вы не являетесь заказчиком этой заданий"))

        # Check if the orderer is not worker
        if orderer == task.worker:
            raise ValidationError(_("Вы не можете оценивать себя как заказчика"))

        return validated_data
