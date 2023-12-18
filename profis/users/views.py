from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.views import (
    LoginView,  # , LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import RedirectView
from drf_spectacular.utils import extend_schema

# from phonenumbers import PhoneNumber
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from profis.users.models import PhoneNumber
from profis.users.serializers import (
    PasswordResetConfirmOTPSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    PhoneNumberSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSerializer,
)
from profis.users.tasks import send_otp_by_email, send_otp_by_phone

User = get_user_model()


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        "password",
        "old_password",
        "new_password1",
        "new_password2",
    ),
)


@extend_schema(tags=["auth"])
class UserRegisterView(RegisterView):
    """
    Register new users using phone number or email and password.
    """

    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = request.data.get("phone_number", None)
            email = request.data.get("email", None)
            if phone_number:
                otp = str(serializer.validated_data["otp"])
                cached_otp = cache.get(phone_number)
                if cached_otp:
                    if cached_otp == otp:
                        user = self.perform_create(serializer)
                        headers = self.get_success_headers(serializer.data)

                        # Create phone number for current user
                        PhoneNumber.objects.create(user=user, phone_number=phone_number, is_verified=True)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                    else:
                        response_data = {"message": _("Введен неправильный код")}
                        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    response_data = {"message": _("Срок действия кода истек или не отправлен")}
                    return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
            elif email:
                user = self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=["auth"])
class UserLoginAPIView(LoginView):
    """
    Authenticate existing users using phone number or email and password.
    """

    serializer_class = UserLoginSerializer


@extend_schema(tags=["auth"])
class PasswordResetAPIView(GenericAPIView):
    """
    Use this to send otp to email or phone number only for password resetting
    """

    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]
    throttle_scope = "dj_rest_auth"

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = request.data.get("phone_number", None)
            email = request.data.get("email", None)
            otp = get_random_string(length=4, allowed_chars="0123456789")
            if phone_number is not None:
                cache.set(key=phone_number, value=otp, timeout=60)
                send_otp_by_phone.delay(phone_number=phone_number, otp=otp)
            elif email is not None:
                cache.set(key=email, value=otp, timeout=60)
                send_otp_by_email.delay(otp=otp, email=email)

            response_data = {"detail": _("Код отправлен")}
            return Response(data=response_data, status=status.HTTP_200_OK)


@extend_schema(tags=["auth"])
class PasswordResetConfirmOTPAPIView(GenericAPIView):
    """
    Confirm sent otp for password resetting
    """

    serializer_class = PasswordResetConfirmOTPSerializer
    permission_classes = [AllowAny]
    throttle_scope = "dj_rest_auth"

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = request.data.get("phone_number", None)
            email = request.data.get("email", None)
            otp = request.data.get("otp", None)

            if phone_number is not None:
                cached_otp = cache.get(key=phone_number)
            elif email is not None:
                cached_otp = cache.get(key=email)

            if cached_otp and cached_otp == otp:
                response_data = {"detail": _("Код успешно подтвержден")}
                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "Срок действия кода истек или недействителен"}, status=status.HTTP_400_BAD_REQUEST
                )


@extend_schema(tags=["auth"])
class PasswordResetConfirmAPIView(GenericAPIView):
    """
    Set new password
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]
    throttle_scope = "dj_rest_auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password")},
        )

    # def post(self, request, *args, **kwargs):
    #     # Create a serializer with request.data
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         phone_number = request.data.get("phone_number", None)
    #         email = request.data.get("email", None)
    #         otp = request.data.get("otp", None)

    #         if phone_number is not None:
    #             cached_otp = cache.get(key=phone_number)
    #         elif email is not None:
    #             cached_otp = cache.get(key=email)

    #         if cached_otp and cached_otp == otp:
    #             response_data = {"detail": _("Код успешно подтвержден")}
    #             return Response(data=response_data, status=status.HTTP_200_OK)
    #         else:
    #             return Response(
    #                 {"detail": "Срок действия кода истек или недействителен"}, status=status.HTTP_400_BAD_REQUEST
    #             )


@extend_schema(tags=["users"])
class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    # def get_queryset(self, *args, **kwargs):
    #     assert isinstance(self.request.user.id, int)
    #     return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


@extend_schema(tags=["users"])
class WorkerListViewSet(ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        if "category_slug" in self.kwargs:
            category = self.kwargs["category_slug"]
            return self.queryset.filter(is_worker=True, categories__slug=category)
        return self.queryset.filter(is_worker=True)


@extend_schema(tags=["auth"])
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/api/users/"
    client_class = OAuth2Client


@extend_schema(tags=["auth"])
class SendSMSAPIView(GenericAPIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """

    serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        # Send OTP
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = str(serializer.validated_data["phone_number"])

            otp = get_random_string(length=4, allowed_chars="0123456789")
            cache.set(key=phone_number, value=otp, timeout=60)
            send_otp_by_phone.delay(phone_number=phone_number, otp=otp)
            response_data = {"message": _("Код отправлен")}
            return Response(data=response_data, status=status.HTTP_200_OK)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"
