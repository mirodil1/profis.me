from django.contrib.gis.geos import Point
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers, validators
from rest_framework_gis.serializers import GeoModelSerializer

from profis.categories.models import Category
from profis.categories.serializers import CategorySerializer
from profis.subscription.models import UserPlan
from profis.tasks.models import Task, TaskAddress, TaskImage, TaskResponse, TaskResponseTemplate
from profis.users.serializers import UserSerializer


class TaskAddressSerializer(GeoModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = TaskAddress
        geo_field = "coords.coordinates"
        fields = ["id", "name", "coords", "longitude", "latitude", "point"]


class TaskImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = TaskImage
        fields = [
            "id",
            "image",
        ]


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    owner = UserSerializer()
    file = serializers.FileField(read_only=True)
    images = TaskImageSerializer(many=True)
    address = TaskAddressSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "category",
            "owner",
            "name",
            "description",
            "phone_number",
            "file",
            "status",
            "start_time",
            "finish_time",
            "images",
            "address",
            "number_of_views",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    file = serializers.FileField(required=False)
    address = TaskAddressSerializer(many=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = TaskImageSerializer(many=True)

    class Meta:
        model = Task

        fields = [
            "id",
            "category",
            "owner",
            "name",
            "description",
            "phone_number",
            "file",
            "images",
            "address",
            "start_time",
            "finish_time",
        ]

    def create(self, validated_data):
        images = validated_data.pop("images", None)
        addresses = validated_data.pop("address", None)
        task = Task.objects.create(**validated_data)
        if addresses:
            for address in addresses:
                address = dict(address)
                point = Point(address["latitude"], address["longitude"])
                TaskAddress.objects.create(
                    task=task,
                    name=address["name"],
                    coords=point,
                    point=address["point"],
                )
        if images:
            for image in images:
                TaskImage.objects.create(task=task, image=image)
        return task

    def update(self, instance, validated_data):
        images = validated_data.pop("images", None)
        addresses = validated_data.pop("address", None)
        obj_mapping = {obj.id: obj for obj in instance.images.all()}

        if images:
            for img in images:
                if "id" not in img:
                    # Create new image
                    TaskImage.objects.create(task=instance, image=img["image"])
            for obj_id, obj in obj_mapping.items():
                if obj_id not in [img.get("id") for img in images]:
                    obj.delete()

        if addresses:
            obj_mapping = {obj.id: obj for obj in instance.address.all()}
            for address in addresses:
                if "id" in address:
                    # Update existing address
                    obj_id = address["id"]
                    obj = obj_mapping.get(obj_id, None)
                    if obj is not None:
                        obj.name = address["name"]
                        obj.longitude = address["longitude"]
                        obj.latitude = address["latitude"]
                        obj.point = address["point"]
                        obj.save()
                else:
                    # Create new address
                    if not TaskAddress.objects.filter(task=instance, point=address["point"]).exists():
                        TaskAddress.objects.create(
                            task=instance,
                            name=address["name"],
                            latitude=address["latitude"],
                            longitude=address["longitude"],
                            point=address["point"],
                        )
                    else:
                        raise serializers.ValidationError(_("Адрес с той же задачей и точкой уже существует"))
            for obj_id, obj in obj_mapping.items():
                if obj_id not in [address.get("id") for address in addresses]:
                    obj.delete()
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class TaskForTaskResponseSerializer(serializers.ModelSerializer):
    """
    Use for taskresponse serializer only with necessary fields.
    """

    class Meta:
        model = Task
        fields = ["id"]


class TaskResponseSerializer(serializers.ModelSerializer):
    task = TaskForTaskResponseSerializer()
    worker = UserSerializer()

    class Meta:
        model = TaskResponse
        fields = ["id", "task", "worker", "price", "text", "status", "response_type"]


class TaskResponseCreateSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True)
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskResponse
        fields = ["task", "worker", "price", "text", "status", "response_type"]
        validators = [
            validators.UniqueTogetherValidator(
                queryset=TaskResponse.objects.all(),
                fields=["worker", "task"],
                message=_("`Исполнитель` и `задание` должны быть уникальными"),
            )
        ]

    def validate(self, validated_data):
        task = validated_data.get("task", None)
        worker = validated_data.get("worker", None)
        response_type = validated_data.get("response_type", None)

        if worker and task:
            user_balance = worker.userwallet.balance
            price = task.category.price
            post_price = task.category.post_price

        if not task.status == Task.Status.OPEN:
            raise serializers.ValidationError(_("Задание не активно"))

        if worker == task.owner:
            raise serializers.ValidationError(_("Вы не можете выполнить свою задачу"))

        if response_type:
            if response_type == TaskResponse.ResponseType.PLAIN:
                if user_balance < price:
                    raise serializers.ValidationError(_("Недостаточно средств"))

            elif response_type == TaskResponse.ResponseType.POST:
                if user_balance < post_price:
                    raise serializers.ValidationError(_("Недостаточно средств"))

            elif response_type == TaskResponse.ResponseType.UNLIM:
                if not worker.userplan_set.filter(
                    plan_type=UserPlan.PlanType.UNLIM,
                    expired_at__gt=timezone.now(),
                    categories__in=[task.category, task.category.parent_category],
                ).exists():
                    raise serializers.ValidationError(_("У вас нет активных тарифов"))

            elif response_type == TaskResponse.ResponseType.BASE:
                if not worker.userplan_set.filter(
                    plan_type=UserPlan.PlanType.BASE,
                    categories=task.category.parent_category,
                    expired_at__gt=timezone.now(),
                ).exists():
                    raise serializers.ValidationError(_("У вас нет активных тарифов"))
        return validated_data


class TaskResponseTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for task template model
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskResponseTemplate
        fields = ["user", "title", "description"]
