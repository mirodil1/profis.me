from rest_framework import serializers

from profis.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    params = serializers.JSONField()
    method = serializers.CharField()

    class Meta:
        model = Transaction
        fields = [
            "user_id",
            "amount",
            "state",
            "status",
            "create_time",
            "perform_time",
            "cancel_time",
            "reason",
            "params",
            "method",
        ]
