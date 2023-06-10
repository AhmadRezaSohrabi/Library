from django.db import models
from base.models import BaseAbstractModel


class Staff(BaseAbstractModel):
    owner = models.OneToOneField(
        to="user.User",
        null=False,
        blank=False,
        related_name="staff",
        related_query_name="staff",
        on_delete=models.PROTECT
    )
    name = models.CharField(
        max_length=63
    )