from django.contrib import admin
from django.utils.safestring import mark_safe

from profis.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "icon_tag",
    ]
    search_fields = [
        "name",
    ]
    exclude = [
        "slug",
    ]

    @admin.display(description="Иконка")
    def icon_tag(self, obj):
        return mark_safe('<img src="%s" width="32" height="32" />' % (obj.icon.url))
