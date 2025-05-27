from django.db import models

    # models.py
class Transaction(models.Model):
    buy_order = models.CharField(max_length=26, unique=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)