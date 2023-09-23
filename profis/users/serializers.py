from django.contrib.auth import get_user_model
from rest_framework import serializers

from profis.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    avatar = serializers.ImageField(read_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "bio",
            "age",
            "number_of_views",
            "is_worker",
            "avatar",
            "work_experiance",
            "gender",
        ]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "bio",
            "date_of_birth",
            "avatar",
            "is_worker",
            "work_experiance",
            "gender",
        ]
