from django.contrib import admin
from book.models import (
    Book,
    BookCategory, 
    BookBorrow
)
# Register your models here.

admin.site.register(Book)
admin.site.register(BookCategory)
admin.site.register(BookBorrow)
