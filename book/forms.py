from typing import Any, Dict
from django import forms
from customer.models import Customer

class BorrowBookForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.eager_load_wallet())


class SellBookForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.eager_load_wallet())
