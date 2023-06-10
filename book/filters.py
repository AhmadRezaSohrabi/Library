from django_filters import FilterSet, BaseRangeFilter, NumberFilter
from book.models import Book


class NumberRangeFilter(BaseRangeFilter, NumberFilter):
    pass


class BookFilter(FilterSet):
    purchase_stock = NumberRangeFilter(field_name='purchase_stock', lookup_expr='range')
    borrow_stock = NumberRangeFilter(field_name='borrow_stock', lookup_expr='range')

    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "author": ["icontains"],
            "category__title": ["icontains"],
        }
