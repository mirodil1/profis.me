from typing import Any

from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from profis.categories.models import Category
from profis.users.exceptions import AccountDisabledException, InvalidCredentialsException
from profis.users.models import PhoneNumber
from profis.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    avatar = serializers.ImageField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    rating = serializers.SerializerMethodField()

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
            "rating",
        ]

    def get_rating(self, obj):
        return obj.rating


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user
    """

    categories = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(
            queryset=Category.objects.all(),
            required=True,
        ),
    )

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

    def update(self, instance, validated_data):
        categories = validated_data.pop("categories", [])
        instance.categories.set(categories)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class UserWorkerRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting to get worker status
    """

    categories = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(
            queryset=Category.objects.all(),
            required=True,
            write_only=True,
        ),
    )
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    middle_name = serializers.CharField(required=True, write_only=True)
    bio = serializers.CharField(required=True, write_only=True)
    date_of_birth = serializers.DateField(required=True, write_only=True)
    phone_number = PhoneNumberField(required=True, write_only=True)
    otp = serializers.CharField(required=False, write_only=True)

    def validate(self, validated_data):
        user = self.context["request"].user
        if user.is_worker:
            raise serializers.ValidationError(_("Вы уже получили статус исполнителя"))
        if all(validated_data):
            print(True)
        return super().validate(validated_data)


class UserRegisterSerializer(RegisterSerializer):
    """
    Serializer for registrating new users using email or phone number.
    """

    username = None
    phone_number = PhoneNumberField(
        required=False,
        validators=[
            UniqueValidator(
                queryset=PhoneNumber.objects.all(), message=_("A user has already registered with this phone number.")
            )
        ],
    )
    email = serializers.EmailField(
        required=False,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message=_("A user has already registered with this email."))
        ],
    )
    first_name = serializers.CharField(max_length=64, required=True)
    last_name = serializers.CharField(max_length=64, required=True)
    otp = serializers.CharField(required=False, write_only=True)

    def validate(self, validated_data):
        email = validated_data.get("email", None)
        phone_number = validated_data.get("phone_number", None)
        first_name = validated_data.get("first_name", None)
        last_name = validated_data.get("last_name", None)

        if not (email or phone_number):
            raise serializers.ValidationError(_("Введите адрес электронной почты или номер телефона."))

        if not (first_name and last_name):
            raise serializers.ValidationError(_("Введите имя и фамилию"))

        return validated_data

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["phone_number"] = self.validated_data.get("phone_number", None)
        data["first_name"] = self.validated_data.get("first_name", None)
        data["last_name"] = self.validated_data.get("last_name", None)
        data["email"] = self.validated_data.get("email", None)
        return data


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer to login users with email or phone number.
    """

    phone_number = PhoneNumberField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def _validate_phone_email(self, phone_number, email, password):
        user = None

        if email and password:
            user = authenticate(username=email, password=password)
        elif str(phone_number) and password:
            user = authenticate(username=str(phone_number), password=password)
        else:
            raise serializers.ValidationError(_("Введите номер телефона или адрес электронной почты и пароль"))

        return user

    def validate(self, validated_data):
        phone_number = validated_data.get("phone_number")
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = None

        user = self._validate_phone_email(phone_number, email, password)

        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()

        if phone_number:
            if not user.phone.is_verified:
                raise serializers.ValidationError(_("Номер телефона не подтвержден."))

        validated_data["user"] = user
        return validated_data


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message=_("A user is already registered with this phone number.")
            )
        ],
    )


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset otp.
    """

    email = serializers.EmailField(required=False, write_only=True)
    phone_number = PhoneNumberField(required=False, write_only=True)

    def validate(self, validated_data) -> Any:
        email = validated_data.get("email", None)
        phone_number = validated_data.get("phone_number", None)

        if not (email or phone_number):
            raise serializers.ValidationError(_("Введите адрес электронной почты или номер телефона."))
        if email is not None:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": _("Пользователь не найден")})
        elif phone_number is not None:
            if not User.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError({"phone_number": _("Пользователь не найден")})

        return validated_data


class PasswordResetConfirmOTPSerializer(serializers.Serializer):
    """
    Serializer for confirming an otp.
    """

    email = serializers.EmailField(required=False, write_only=True)
    phone_number = PhoneNumberField(required=False, write_only=True)
    otp = serializers.CharField(required=True, write_only=True)

    def validate(self, validated_data):
        email = validated_data.get("email", None)
        phone_number = validated_data.get("phone_number", None)
        otp = validated_data.get("otp", None)

        if not (email or phone_number):
            raise serializers.ValidationError(_("Введите адрес электронной почты или номер телефона."))
        if not otp:
            raise serializers.ValidationError({"otp": _("Обязательное поле")})

        return validated_data


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset attempt.
    """

    new_password1 = serializers.CharField(max_length=128, write_only=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(required=False, write_only=True)
    phone_number = PhoneNumberField(required=False, write_only=True)

    set_password_form_class = SetPasswordForm

    user = None
    set_password_form = None

    def validate(self, validated_data):
        email = validated_data.get("email", None)
        phone_number = validated_data.get("phone_number", None)

        if not (email or phone_number):
            raise serializers.ValidationError(_("Введите адрес электронной почты или номер телефона."))

        try:
            if email:
                self.user = User._default_manager.get(email=email)
            elif phone_number:
                self.user = User._default_manager.get(phone_number=phone_number)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError(_("Пользователь не найден"))

        self.set_password_form = self.set_password_form_class(
            user=self.user,
            data=validated_data,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return validated_data

    def save(self):
        return self.set_password_form.save()


# class PhoneNumberSerializer(serializers.ModelSerializer):
#     """
#     Serializer class to serialize phone number.
#     """
#     phone_number = PhoneNumberField()

#     class Meta:
#         model = PhoneNumber
#         fields = ('phone_number',)

#     def validate_phone_number(self, value):
#         try:
#             queryset = User.objects.get(phone__phone_number=value)
#             if queryset.phone.is_verified == True:
#                 err_message = _('Phone number is already verified')
#                 raise serializers.ValidationError(err_message)

#         except User.DoesNotExist:
#             raise AccountNotRegisteredException()

#         return value
