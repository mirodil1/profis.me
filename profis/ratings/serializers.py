from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError

from profis.ratings.models import TaskRating
from profis.tasks.models import Task

User = get_user_model()


class TaskRatingSerializer(serializers.ModelSerializer):
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


class TaskRatingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for rating worker of the tasks
    """

    orderer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True, required=True)
    worker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=True)

    class Meta:
        model = TaskRating
        validators = [
            validators.UniqueTogetherValidator(
                queryset=TaskRating.objects.all(),
                fields=["orderer", "task"],
                message=_("Рейтинг с той же задачей и исполнителем уже существует"),
            )
        ]
        fields = [
            "worker",
            "orderer",
            "task",
            "score",
            "review",
        ]

    def validate(self, validated_data):
        orderer = validated_data.get("orderer")
        task = validated_data.get("task")
        score = validated_data.get("score")

        # Check if the worker is not orderer (owner of the task)
        if orderer == task.worker:
            raise ValidationError(_("Вы не можете оценивать себя как исполнителя"))

        # Check if the worker is related to this task
        if orderer != task.owner:
            raise ValidationError(_("Вы не являетесь заказчиком этой заданий"))

        # Allowed score
        if score:
            if score < 0 or score > 5:
                raise ValidationError(_("Допустимый балл составляет от 1 до 5"))

        return validated_data
