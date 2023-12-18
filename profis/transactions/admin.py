from django.contrib import admin

from profis.transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["_id", "user_id", "amount", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["user_id", "_id"]
