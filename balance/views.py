from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.contrib.auth.models import User
from .models import Balance, Transaction
from .serializers import BalanceSerializer, TransactionSerializer


class BalanceView(generics.RetrieveAPIView):
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.balance


class AddBalanceView(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            balance = request.user.balance
            balance.amount += serializer.data['amount']
            balance.save()
        return Response({})


class TransferView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.data['amount']
        to_user_id = serializer.data['to_user']

        to_user = User.objects.get(id=to_user_id)

        with transaction.atomic():
            from_balance = request.user.balance
            to_balance = to_user.balance

            if from_balance.amount < amount:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

            from_balance.amount -= amount
            to_balance.amount += amount

            from_balance.save()
            to_balance.save()

            _transaction = Transaction.objects.create(
                from_user=request.user,
                to_user=to_user,
                amount=amount
            )

        return Response(TransactionSerializer(_transaction).data)


class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            Q(from_user=user) | Q(to_user=user)
        )
