from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required


from customer.views import (
    CustomerBoughtBookListView,
    CustomerBorrowedBookListView,
    CustomerListView
    
)

urlpatterns = [
    path(
        '',
        CustomerListView.as_view(),
        name='list_customers'
    ),
    path(
        '<int:pk>/borrowed_books/',
        CustomerBorrowedBookListView.as_view(),
        name='list_customer_borrowed_books'
    ),
    path(
        '<int:pk>/bought_books/',
        CustomerBoughtBookListView.as_view(),
        name='list_customer_bought_books'
    ),
]