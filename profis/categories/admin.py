from typing import Any

from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe

from profis.categories.models import Category


class CategoryChildInline(admin.StackedInline):
    model = Category
    extra = 1


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = [
        "order",
        "name",
        "parent_category",
        "icon_tag",
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
