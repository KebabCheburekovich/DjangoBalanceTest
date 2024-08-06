from django.urls import path
from .views import BalanceView, AddBalanceView, TransferView, TransactionHistoryView

urlpatterns = [
    path('balance/', BalanceView.as_view(), name='balance'),
    path('balance/add/', AddBalanceView.as_view(), name='add_balance'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transfer/history', TransactionHistoryView.as_view(), name='transfer_history'),
]
