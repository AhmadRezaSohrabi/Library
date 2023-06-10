from django.db import models
from django.db.models.query import QuerySet

class BaseManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class BaseAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = BaseManager()

    class Meta:
        abstract = True