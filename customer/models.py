from django.db import models
from base.models import BaseAbstractModel, BaseManager

from accounting.models import Wallet

class CustomerManager(BaseManager):

    def eager_load_all(self):
        return self.get_queryset()\
                    .select_related("category")\
                    .prefetch_related("borrowers", "purchasers")\

    def eager_load_wallet(self):
        return self.get_queryset().select_related("wallet")


class Customer(BaseAbstractModel):
    owner = models.OneToOneField(
        to="user.User",
        null=False,
        blank=False,
        related_name="customer",
        related_query_name="customer",
        on_delete=models.PROTECT
    )
    name = models.CharField(
        max_length=63
    )
    objects = CustomerManager()        

    def save(self, *args, **kwargs):
        if self.wallet is None:
            Wallet.objects.create(customer=self)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Violation(models.Model):
    customer = models.ForeignKey(
        to="customer.Customer",
        related_name="violations",
        related_query_name="violation",
        on_delete=models.CASCADE
    )
    description = models.TextField(
        blank=True
    )
    overdue_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description