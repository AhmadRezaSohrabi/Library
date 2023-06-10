from django.urls import path
from book.views import (
    BorrowBookView,
    BookListView,
    SellBookView,
    CategoryListView
)

urlpatterns = [
    path(
        'books/<int:pk>/borrow/',
        BorrowBookView.as_view(),
        name='borrow_book'
    ),
    path(
        'books/<int:pk>/sell/',
        SellBookView.as_view(),
        name='sell_book'
    ),
    path(
        'books/',
        BookListView.as_view(),
        name='list_books'
    ),
    path(
        'book_categories/',
        CategoryListView.as_view(),
        name='list_books'
    ),
]