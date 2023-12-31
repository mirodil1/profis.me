from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators, get_user_model
from django.utils.translation import gettext_lazy as _

from profis.users.forms import UserAdminChangeForm, UserAdminCreationForm
from profis.users.models import PhoneNumber, UserWallet

User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://django-allauth.readthedocs.io/en/stable/advanced.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


class UserWalletInline(admin.StackedInline):
    model = UserWallet
    # exclude = ["id"]
    # readonly_fields = ["balance"]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (
            _("Персональная информация"),
            {"fields": ("first_name", "last_name", "phone_number", "gender", "date_of_birth")},
        ),
        (
            _("Общая информация"),
            {"fields": ("bio", "categories", "number_of_views", "is_worker", "avatar", "work_experiance")},
        ),
        (
            _("Права доступа"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
        (None, {"fields": ("email", "password")}),
    )
    list_display = [
        "_id",
        "phone_number",
        "first_name",
        "last_name",
        "is_worker",
        "email",
        "is_superuser",
    ]
    list_filter = auth_admin.UserAdmin.list_filter + ("is_worker",)
    search_fields = ["first_name", "last_name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ["number_of_views"]
    inlines = [UserWalletInline]


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "user", "is_verified"]
