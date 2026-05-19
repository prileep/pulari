import re

from django.shortcuts import render,redirect, get_object_or_404

from core.utils.formatter import clean_decimal
from django.db.models import Value
from django.db.models.functions import Concat, Coalesce


from .models import Item

def item_list(request):
    sort = request.GET.get('sort', 'item_rid')

    valid_sorts = [
        'item_rid', '-item_rid',
        'item_name', '-item_name',
        'item_mrp', '-item_mrp',
        'item_stk', '-item_stk'
    ]

    if sort not in valid_sorts:
        sort = 'item_rid'

    items = Item.objects.annotate(
        display_name_calc=Concat(
            'item_name',
            Value(' - '),
            Coalesce('item_code', Value(''))
        )
    ).order_by(sort)

    return render(request, 'items/item_list.html', {
        'items': items,
        'current_sort': sort
    })

# # ITEM
from .models import Item
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
def item(request, pk):

    item_obj = None
    message = None   # 👈 add this

    # 👉 EDIT
    if str(pk) != "0":
        item_obj = get_object_or_404(Item, pk=pk)

    # 👉 SAVE
    if request.method == "POST":
        
        item_name = request.POST.get("item_name")
        

        item_code = request.POST.get("item_code")
        if item_name:
            item_name = item_name.strip().upper()

        if item_code:
            item_code = item_code.strip().upper()

        if not item_name:
            message = "Item name is required"
            return render(request, "items/item.html", {
                "item": item_obj,
                "message": message
            })
        if not item_code:
            message = "Item code is required"
            return render(request, "items/item.html", {
                "item": item_obj,
                "message": message
            })
        
        item_gst = clean_decimal(request.POST.get("item_gst"))
        item_mrp = clean_decimal(request.POST.get("item_mrp"))
        item_sale_price = clean_decimal(request.POST.get("item_sale_price"))
        item_display_name = request.POST.get("item_display_name")
        
        item_stk = clean_decimal(request.POST.get("item_stk"))
        if item_obj:  # update
            item_obj.item_name = item_name
            item_obj.item_code = item_code
            item_obj.item_gst = item_gst
            item_obj.item_mrp = item_mrp
            item_obj.item_sale_price = item_sale_price
            item_obj.item_display_name = item_display_name
            item_obj.item_stk = item_stk
            item_obj.save()
            message = "Item updated successfully ✔"

        else:  # create
            item_obj = Item.objects.create(
                item_name=item_name,
                item_code=item_code,
                item_gst=item_gst,
                item_mrp=item_mrp,
                item_sale_price=item_sale_price,
                item_display_name=item_display_name,
                item_stk=item_stk
                
            )
            message = "Item saved successfully ✔"

            item_obj = None 
    return render(request, 'items/item.html', {
        'item': item_obj,
        'message': message
    })