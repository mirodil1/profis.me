from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from profis.subscription.models import UserPlan


@admin.register(UserPlan)
class Plan(admin.ModelAdmin):
    list_display = ["user", "plan_type", "is_active_icon"]
    list_filter = ["plan_type"]

    @admin.display(description=_("Статус"))
    def is_active_icon(self, obj):
        if obj.is_active:
            return format_html("<img src='/static/admin/img/icon-yes.svg' alt=True>")  # Green checkmark for active
        return format_html("<img src='/static/admin/img/icon-no.svg' alt=True>")  # Red X for inactive
