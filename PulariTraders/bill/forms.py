from django import forms
from .models import BillHeader, BillDetail


class BillHeaderForm(forms.ModelForm):
    class Meta:
        model = BillHeader
        db_table = 'bill_header'
        fields = [
            'bh_bill_no',
            'bh_bill_date',
            'bh_acc_rid',
            'bh_notes',
            'bh_counter_sale',
        ]
        widgets = {
            'bh_bill_date': forms.DateInput(attrs={'type': 'date'}),
            'bh_notes': forms.TextInput(attrs={'maxlength': 120}),
        }


class BillDetailForm(forms.ModelForm):
    class Meta:
        model = BillDetail
        db_table = 'bill_detail'
        fields = [
            'bd_quantity',
            'bd_amount',
            'bd_total_amount',
        ]
from django.forms import inlineformset_factory
from .models import BillHeader, BillDetail
BillDetailFormSet = inlineformset_factory(
    BillHeader,
    BillDetail,
    form=BillDetailForm,
    extra=5,
    can_delete=True
)