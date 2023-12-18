from django.urls import path

from profis.transactions.views import TransactionAPIView

app_name = "transactions"
urlpatterns = [
    path("payme", TransactionAPIView.as_view(), name="pay"),
]
