from django_tables2 import SingleTableView

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.db import transaction

from book.models import Book, BookCategory
from book.forms import BorrowBookForm, SellBookForm
from book.tables import BookTable, BookCategoryTable
from customer.models import Customer


class BorrowBookView(View):
    form_class = BorrowBookForm
    initial = {}
    template_name = "borrow_book.html"

    def get(self, request, *args, **kwargs):
        borrow_book_form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"borrow_book_form": borrow_book_form})

    def _validate_and_get_error_message(
            self,
            book: Book,
            customer: Customer, 
    ): # Can be handled in a Validation class, ignored due to lack of time :(
        if book.borrow_stock == 0:
            return "Stock is empty"

        if book.is_borrowed_to_customer(customer):
            return "Already borrowed"
        
        if book.category.borrow_cost * 3 > customer.wallet.balance:
            return "Not enough wallet balance(at least three days of daily cost must be available)"

        # if customer.category_borrowed_books(book.category).count() < book.category.permitted_borrow_count:
        #     return "You have passed the limit for borrowing book of this category"

        return

    def post(self, request, *args, **kwargs):
        request_data = request.POST.copy()
        customer = request_data.pop("customer")[0]
        borrow_book_form = self.form_class(
            {
                **request_data,
                "customer": customer,
            }
        )
        if borrow_book_form.is_valid():

            with transaction.atomic():
                customer = borrow_book_form.cleaned_data['customer']
                book: Book = Book.objects.eager_load_category().get(pk=self.kwargs["pk"])
                error_message = self._validate_and_get_error_message(
                    book=book,
                    customer=customer,
                )
                if error_message is not None:
                    messages.error(request, message=error_message)
                    return render(request, self.template_name, {"borrow_book_form": borrow_book_form})

                book.borrow(customer=customer)

            return redirect("list_books")

        return render(request, self.template_name, {"borrow_book_form": borrow_book_form})



class SellBookView(View):
    form_class = SellBookForm
    initial = {}
    template_name = "sell_book.html"

    def get(self, request, *args, **kwargs):
        sell_book_form = self.form_class(initial=self.initial)
        print(sell_book_form)
        return render(request, self.template_name, {"sell_book_form": sell_book_form})

    def _validate_and_get_error_message(
            self,
            book: Book,
            customer: Customer, 
        ): # Can be handled in a Validation class, ignored due to lack of time :(
        if book.purchase_stock == 0:
            return "Stock is empty"

        if book.price > customer.wallet.balance:
            return "Wallet balance is not enough"

        return

    def post(self, request, *args, **kwargs):
        request_data = request.POST.copy()
        customer = request_data.pop("customer")[0]
        sell_book_form = self.form_class(
            {
                **request_data,
                "customer": customer,
            }
        )
        if sell_book_form.is_valid():

            with transaction.atomic():
                customer = sell_book_form.cleaned_data['customer']
                book: Book = Book.objects.eager_load_category().get(pk=self.kwargs["pk"])
                error_message = self._validate_and_get_error_message(
                    book=book,
                    customer=customer,
                )
                if error_message is not None:
                    messages.error(request, message=error_message)
                    return render(request, self.template_name, {"sell_book_form": sell_book_form})

                book.sell(customer=customer)


            return redirect("list_books")

        return render(request, self.template_name, {"sell_book_form": sell_book_form})


class BookListView(SingleTableView):
    template_name = "list_books.html"
    table_class = BookTable
    queryset = Book.objects.eager_load_category()
    model = Book


class CategoryListView(SingleTableView):  # Shows the income too
    template_name = "list_book_categorys.html"
    table_class = BookCategoryTable
    model = BookCategory
