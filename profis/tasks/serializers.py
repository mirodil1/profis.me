from rest_framework import serializers

from profis.categories.models import Category
from profis.categories.serializers import CategorySerializer
from profis.tasks.models import Task, TaskImage, TaskResponse
from profis.users.serializers import UserSerializer


class TaskImageSerializer(serializers.ModelSerializer):
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
            "number_of_views",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    file = serializers.FileField(write_only=True, required=False)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
            "uploaded_images",
            "start_time",
            "finish_time",
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        task = Task.objects.create(**validated_data)
        if uploaded_images:
            for image in uploaded_images:
                TaskImage.objects.create(task=task, image=image)
        return task

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        print(uploaded_images)
        # if uploaded_images is not None:
        #     print(uploaded_images)
        #     obj_mapping = {obj.id: obj for obj in instance.images.all()}
        #     for img in uploaded_images:
        #         if "id" in img:
        #             print(obj.image)
        #             # Update existing object
        #             obj_id = img["id"]
        #             obj = obj_mapping.get(obj_id, None)
        #             if obj is not None:
        #                 obj.image = img
        #                 obj.save()
        #         else:
        #             # Create new object
        #             TaskImage.objects.create(
        #                 task=instance,
        #                 image=img
        #             )
        # Update remaining fields of TutorProfileSerializer
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
        fields = ["id", "task", "worker", "price", "text", "status"]


class TaskResponseCreateSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True)
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskResponse
        fields = ["task", "worker", "price", "text", "status"]
