import django_tables2 as tables

from book.models import Book, BookCategory


class BookTable(tables.Table):
    borrow = tables.LinkColumn(
          'borrow_book', 
          args= [tables.A('pk')], 
          attrs= {
            'a': {'class': 'btn btn-primary'}
          },
          text='borrow book',
    )
  
    sell = tables.LinkColumn(
          'sell_book', 
          args= [tables.A('pk')], 
          attrs= {
            'a': {'class': 'btn btn-primary'}
          },
          text='sell book',
    )
    category__title  = tables.Column(
        verbose_name="Category Title"
    )


    class Meta:
        model = Book
        fields = (
          'title',
          'author',
          'category__title',
          'purchase_stock', 
          'borrow_stock'
        )


class MinimalBookTable(tables.Table):
    category__title  = tables.Column(
        verbose_name="Category Title"
    )

    class Meta:
        model = Book
        fields = (
          'title',
          'author',
          'category__title',
        )


class BookCategoryTable(tables.Table):
    
    class Meta:
        model = BookCategory
        fields = (
            "title",
            "permitted_borrow_count",
            "borrow_cost",
            "income"
        )