from typing import Any

from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from profis.categories.models import Category


class CategoryChildInline(admin.StackedInline):
    model = Category
    exclude = ["slug"]
    fieldsets = (
        (
            _("Общая информация"),
            {"fields": ("name", "parent_category", "icon", "price")},
        ),
        (
            _("base"),
            {"fields": ("base_price_25", "base_price_50", "base_price_100")},
        ),
        (
            _("unlim"),
            {"fields": ("unlim_price_15", "unlim_price_30", "unlim_price_90")},
        ),
    )
    extra = 1


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (
            _("Общая информация"),
            {"fields": ("name", "parent_category", "icon", "price", "post_price")},
        ),
        (
            _("Базовый тариф"),
            {"fields": ("base_price_25", "base_price_50", "base_price_100")},
        ),
        (
            _("Безлимитный тариф"),
            {"fields": ("unlim_price_15", "unlim_price_30", "unlim_price_90")},
        ),
    )
    list_display = [
        "order",
        "name",
        "parent_category",
        "icon_tag",
        "price",
    ]
    search_fields = [
        "name",
    ]
    exclude = [
        "slug",
    ]
    inlines = [CategoryChildInline]

    @admin.display(description="Иконка")
    def icon_tag(self, obj):
        return mark_safe('<img src="%s" width="32" height="32" />' % (obj.icon.url))

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        return qs.filter(parent_category=1)
