from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_rid', 'item_name', 'item_code', 'item_gst', 'item_mrp', 'item_sale_price']