# Generated by Django 4.2.1 on 2023-06-10 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="owner",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="customer",
                related_query_name="customer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]