# Generated by Django 4.2.1 on 2023-06-10 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("customer", "0001_initial"),
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookpurchase",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="book_purchases",
                related_query_name="book_purchase",
                to="customer.customer",
            ),
        ),
        migrations.AddField(
            model_name="bookborrow",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="c",
                related_query_name="book_borrow",
                to="book.book",
            ),
        ),
        migrations.AddField(
            model_name="bookborrow",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="book_borrows",
                related_query_name="book_borrow",
                to="customer.customer",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="borrowers",
            field=models.ManyToManyField(
                related_name="borrowed_books",
                related_query_name="borrowed_book",
                through="book.BookBorrow",
                to="customer.customer",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="books",
                related_query_name="book",
                to="book.bookcategory",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="purchasers",
            field=models.ManyToManyField(
                related_name="purchased_books",
                related_query_name="purchased_book",
                through="book.BookPurchase",
                to="customer.customer",
            ),
        ),
    ]
