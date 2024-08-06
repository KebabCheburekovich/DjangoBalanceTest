from django.contrib.auth.models import User
from django.db import models, transaction


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)


class Transaction(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
