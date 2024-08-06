from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Balance, Transaction


class AmountValidate:
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount must be positive")
        return value


class BalanceSerializer(serializers.ModelSerializer, AmountValidate):
    class Meta:
        model = Balance
        fields = ['amount']


class TransactionSerializer(serializers.ModelSerializer, AmountValidate):
    class Meta:
        model = Transaction
        fields = ['from_user', 'to_user', 'amount', 'timestamp']
