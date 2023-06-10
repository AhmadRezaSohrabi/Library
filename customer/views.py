from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin

from book.models import Book
from book.filters import BookFilter
from book.tables import MinimalBookTable

from customer.models import Customer
from customer.tables import CustomerTable


class CustomerBorrowedBookListView(SingleTableMixin, FilterView):
    template_name = "list_customer_borrowed_books.html"
    table_class = MinimalBookTable
    filterset_class = BookFilter
    model = Book

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(borrowers__id=self.kwargs["pk"]).distinct()


class CustomerBoughtBookListView(SingleTableMixin, FilterView):
    template_name = "list_customer_bought_books.html"
    table_class = MinimalBookTable
    filterset_class = BookFilter
    model = Book

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(purchasers__id=self.kwargs["pk"])


class CustomerListView(SingleTableView):
    template_name = "list_customers.html"
    table_class = CustomerTable
    model = Customer