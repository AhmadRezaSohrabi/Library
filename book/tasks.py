
from django.db.models import OuterRef

from base.sql import SubquerySum
from library.celery import app
from accounting.models import Transaction
from customer.models import Violation
from book.models import BookCategory, BookBorrow


@app.task(name="borrow_daily_fee_collection")
def borrow_daily_fee_collection():
    active_borrows = BookBorrow.objects.filter(return_datetime__isnull=True).select_related(
        "customer", "customer__wallet"
    )
    book_borrow: BookBorrow
    for book_borrow in active_borrows:
        book_borrow.customer.wallet.withdraw(book_borrow.daily_cost)
        if book_borrow.is_overdue:
            Violation.objects.create(
                customer=book_borrow.customer,
                description="Book borrow overdue"
            )


    


@app.task(name="calculate_category_income")
def calculate_category_income():
    BookCategory.objects.all().update(
        income=SubquerySum(
                Transaction.objects.filter(
                    wallet__customer__borrowed_book__category=OuterRef("pk"),
                    is_deposit=False
            ),
            "quantity"
        ) + SubquerySum(
                        Transaction.objects.filter(
                    wallet__customer__purchased_book__category=OuterRef("pk"),
                    is_deposit=False
            ),
            "quantity"
        )
    )