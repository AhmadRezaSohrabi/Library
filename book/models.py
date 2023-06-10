from decimal import Decimal
from datetime import timedelta, datetime
from django.db import models
from base.models import BaseAbstractModel, BaseManager


class BookCategory(models.TextChoices):
    FICTION = 'fiction', 'Fiction'
    NON_FICTION = 'non-fiction', 'Non-Fiction'
    SCI_FI = 'sci-fi', 'Science Fiction'
    FANTASY = 'fantasy', 'Fantasy'
    MYSTERY = 'mystery', 'Mystery'
    ROMANCE = 'romance', 'Romance'


class BookCategory(models.Model):
    title = models.CharField(
        max_length=20,
        choices=BookCategory.choices
    )
    permitted_borrow_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    borrow_cost = models.FloatField(
        null=True,
        blank=True
    )
    income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0)
    )


class BookManager(BaseManager):

    def eager_load_all(self):
        return self.get_queryset()\
                    .select_related("category")\
                    .prefetch_related("borrowers", "purchasers")\

    def eager_load_category(self):
        return self.get_queryset().select_related("category")


class Book(BaseAbstractModel):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=64)
    category = models.ForeignKey(
        to="book.BookCategory",
        related_name="books",
        related_query_name="book",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    borrowers = models.ManyToManyField(
        to="customer.Customer",
        related_name="borrowed_books",
        related_query_name="borrowed_book",
        through="book.BookBorrow",
    )
    purchasers = models.ManyToManyField(
        to="customer.Customer",
        related_name="purchased_books",
        related_query_name="purchased_book",
        through="book.BookPurchase",
    )
    price = models.FloatField(
        null=True,
        blank=True
    )
    purchase_stock = models.PositiveSmallIntegerField(
        default=1
    )
    borrow_stock = models.PositiveSmallIntegerField(
        default=1
    )
    objects = BookManager()

    def is_borrowed_to_customer(self, customer):
        return BookBorrow.objects.filter(
            book=self,
            customer=customer,
            return_datetime__isnull=True
        ).exists()

    def borrow(self, customer):
        book_borrow = BookBorrow.objects.create(book=self, customer=customer)
        self.borrow_stock -= 1
        self.save()
        return book_borrow

    def sell(self, customer):
        book_purchase = BookPurchase.objects.create(book=self, customer=customer)
        self.purchase_stock -= 1
        self.save()
        customer.wallet.withdraw(self.price)
        return book_purchase

    def __str__(self):
        return self.title


class BookBorrow(models.Model):
    customer = models.ForeignKey(
        to="customer.Customer",
        related_name="book_borrows",
        related_query_name="book_borrow",
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        to="book.Book",
        related_name="c",
        related_query_name="book_borrow",
        on_delete=models.CASCADE
    )
    borrow_datetime = models.DateTimeField(
        auto_now_add=True
    )
    allowed_borrow_days = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    return_datetime = models.DateTimeField(
        null=True,
        blank=True
    )
    daily_cost = models.FloatField(
        null=True,
        blank=True
    )

    @property
    def valid_return_datetime(self):
        return self.borrow_datetime + timedelta(
            days=self.allowed_borrow_days
        )

    @property
    def overdue_seconds(self):
        return max(
            (datetime.now() - self.valid_return_datetime).total_seconds(),
            0
        )

    @property
    def is_overdue(self):
        return self.overdue_seconds != 0

    @property
    def is_returned(self):
        return self.return_datetime is not None

    def calculate_borrow_days(self):
        thirty_days_ago = datetime.now() - timedelta(days=30)
        borrows_count = BookBorrow.objects.filter(
            borrow_datetime__gte=thirty_days_ago
        ).count()
        borrow_days =  (30 * self.book.borrow_stock) / (
                self.book.borrow_stock + borrows_count
        ) + 1
        return max(borrow_days, 3)

    def save(self, *args, **kwargs):
        if self.allowed_borrow_days is None:
            self.allowed_borrow_days = self.calculate_borrow_days()
        if self.daily_cost is None:
            self.daily_cost = self.book.category.borrow_cost # pre load book category in select query
        super().save(*args, **kwargs)


class BookPurchase(models.Model):
    customer = models.ForeignKey(
        to="customer.Customer",
        related_name="book_purchases",
        related_query_name="book_purchase",
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        to="book.Book",
        related_name="book_purchases",
        related_query_name="book_purchase",
        on_delete=models.CASCADE
    )
    purchase_datetime = models.DateTimeField(auto_now_add=True)
