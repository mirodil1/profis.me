from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from dj_rest_auth.views import LogoutView  # , PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from profis.users.views import (
    GoogleLogin,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetConfirmOTPAPIView,
    SendSMSAPIView,
    UserLoginAPIView,
    UserRegisterView,
)

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += i18n_patterns(
    # API base url
    path("api/users/", include("profis.users.urls", namespace="users")),
    path("api/categories/", include("profis.categories.urls", namespace="categories")),
    path("api/tasks/", include("profis.tasks.urls", namespace="tasks")),
    path("api/ratings/", include("profis.ratings.urls", namespace="ratings")),
    path("api/subscriptions/", include("profis.subscription.urls", namespace="subscriptions")),
    path("api/chats/", include("profis.chats.urls", namespace="chats")),
    path("api/notifications/", include("profis.notifications.urls", namespace="notifications")),
    path("api/payment/", include("profis.transactions.urls", namespace="transactions")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("dj-rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
    # Auth urls
    path("api/send-sms/", view=SendSMSAPIView.as_view(), name="send-sms"),
    path("api/register/", UserRegisterView.as_view(), name="register"),
    path("api/login/", UserLoginAPIView.as_view(), name="login"),
    # Password reset
    path("api/password/reset/", PasswordResetAPIView.as_view(), name="password-reset"),
    path("api/password/reset/otp/confirm/", PasswordResetConfirmOTPAPIView.as_view(), name="password-confirm-otp"),
    path("api/password/reset/confirm/", PasswordResetConfirmAPIView.as_view(), name="password-reset-confirm"),
    path("resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "account-email-verification-sent/",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    # path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    # path(
    #     "password/reset/confirm/<str:uidb64>/<str:token>",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    prefix_default_language=False,
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
