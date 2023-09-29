from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from profis.categories.serializers import CategorySerializer
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
    categories = CategorySerializer(many=True)

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
            "categories",
        ]


class UserRegisterSerializer(RegisterSerializer):
    """
    Serializer for registrating new users using email or phone number.
    """

    username = None
    phone_number = PhoneNumberField(
        required=True,
        write_only=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message=_("A user is already registered with this phone number.")
            )
        ],
    )
    email = serializers.EmailField(required=False)

    def validate(self, validated_data):
        email = validated_data.get("email", None)
        phone_number = validated_data.get("phone_number", None)

        if not (email or phone_number):
            raise serializers.ValidationError(_("Введите адрес электронной почты или номер телефона."))

        if validated_data["password1"] != validated_data["password2"]:
            raise serializers.ValidationError(_("Пароли не совпадали."))

        return validated_data
