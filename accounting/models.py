from decimal import Decimal
from datetime import datetime
from django.db import models
from base.models import BaseAbstractModel

# Create your models here.
class Wallet(BaseAbstractModel):
    customer = models.OneToOneField(
        to="customer.Customer",
        null=False,
        blank=False,
        related_name="wallet",
        related_query_name="wallet",
        on_delete=models.PROTECT
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0)
    )

    def deposit(self, quantity):
        transaction = Transaction.objects.create(
            wallet=self,
            quantity=quantity,
            created_at=datetime.now(),
            is_deposit=True
        )
        self.balance += Decimal(quantity)
        self.save()
        return transaction

    def withdraw(self, quantity):
        transaction = Transaction.objects.create(
            wallet=self,
            quantity=quantity,
            created_at=datetime.now(),
            is_deposit=False
        )
        self.balance -= Decimal(quantity)
        self.save()
        return transaction


class Transaction(models.Model):
    wallet = models.ForeignKey(
        to="accounting.Wallet",
        related_name="transactions",
        related_query_name="transaction",
        null=False,
        blank=False,
        on_delete=models.PROTECT
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_deposit = models.BooleanField(
        null=False,
        blank=False
    )