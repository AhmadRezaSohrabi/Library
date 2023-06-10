import django_tables2 as tables

from customer.models import Customer

class CustomerTable(tables.Table):
    borrowed_books = tables.LinkColumn(
          'list_customer_borrowed_books', 
          args= [tables.A('pk')], 
          attrs= {
            'a': {'class': 'btn btn-primary'}
          },
          text='borrowed books',
    )
  
    bought_books = tables.LinkColumn(
          'list_customer_bought_books', 
          args= [tables.A('pk')], 
          attrs= {
            'a': {'class': 'btn btn-primary'}
          },
          text='bought books',
    )
    wallet__balance = tables.Column(
        verbose_name="Wallet balance"
    )

    class Meta:
        model = Customer
        fields = (
          "name",
          "wallet__balance"
        )