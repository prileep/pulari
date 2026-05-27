from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date
from django.utils import timezone  # Standard utility for Django tracking

from items.models import Item
from account.models import Account
from django.db.models import Value
from django.db.models.functions import Concat

from .models import BillReturnHeader, BillReturnDetail
from core.utils.formatter import clean_decimal

def get_next_bill_return_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_next_sequence('BillReturn')")
        row = cursor.fetchone()
    return row[0] 

def billreturn(request, rid=None):

    if not rid:
        rid = request.GET.get("rid")

    bill_return_header = BillReturnHeader.empty();
    bill_return_details = []
    account = None

    # ================= CANCEL BILL RETURN =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        with transaction.atomic():
                
            rid = request.POST.get("rid")
            bill_return_header = BillReturnHeader.objects.filter(br_rid=rid).first()

            if bill_return_header: # Good practice to check for None
                bill_return_header.br_status = "Cancelled"
                bill_return_header.br_modified_date = timezone.now() # Update modified date when cancelling
                bill_return_header.save() # This works!

                with connection.cursor() as cursor:
                        cursor.callproc('post_bill_return', [bill_return_header.br_rid])

        messages.success(request, "Bill Return cancelled successfully ❌")

        return redirect(f"/billreturn/{rid}/")

    # ================= LOAD BILL =================
    if rid:
        bill_return_header = BillReturnHeader.objects.filter(br_rid=rid).first()
        bill_return_details = BillReturnDetail.objects.filter(brd_br_rid=rid)

        if bill_return_header:
            account = Account.objects.get(acc_rid=bill_return_header.br_acc_rid)

        for brd in bill_return_details:
            brd.item = Item.objects.get(item_rid=brd.brd_item_rid)

    else:
        bill_return_header = BillReturnHeader.empty()
        billReturn_detail = BillReturnDetail.empty()
        bill_return_details.append(billReturn_detail)

    accounts = Account.objects.filter().values(
        'acc_rid', 'acc_disp_name', 'acc_name',
        'acc_place', 'acc_phone', 'acc_address', 'acc_code'
    )

    items = Item.objects.annotate(
        display_name=Concat('item_name', Value(' - '), 'item_code')
    ).values(
        'item_display_name',
        'item_name',
        'item_code',
        'item_sale_price',
        'item_rid',
        'item_stk'
    )

    # ================= SAVE BILL =================
    if request.method == "POST":

        with transaction.atomic():
            current_timestamp = timezone.now()
            bill_return_header = BillReturnHeader.objects.create(
                br_status='Active',
                br_bill_return_no=get_next_bill_return_no(),
                   
                br_bill_return_date=request.POST.get("br_bill_return_date"),
                br_notes=request.POST.get("br_notes"),
                br_counter_sale=request.POST.get("br_counter_sale"),
                br_acc_rid=request.POST.get("br_acc_rid"),
                br_amount=clean_decimal(request.POST.get("br_amount") or 0),
                br_discount=clean_decimal(request.POST.get("br_discount") or 0),
                br_net_amount=clean_decimal(request.POST.get("br_net_amount") or 0),
                br_created_date=current_timestamp,
                br_modified_date=current_timestamp
            )

            itemRIDs = request.POST.getlist("brd_item_rid")
            quantities = request.POST.getlist("brd_qty")
            amounts = request.POST.getlist("brd_amount")
            brd_total_amounts = request.POST.getlist("brd_total_amount")
            for i in range(len(quantities)):

                qty = quantities[i]
                amt = amounts[i]

                if not qty and not amt:
                    continue

                BillReturnDetail.objects.create(
                    brd_br_rid=bill_return_header.br_rid,
                    brd_item_rid=itemRIDs[i],
                    brd_qty=clean_decimal(qty),
                    brd_amount=clean_decimal(amt),
                    brd_total_amount=clean_decimal(brd_total_amounts[i])
                )

            with connection.cursor() as cursor:
                cursor.callproc('post_bill_return', [bill_return_header.br_rid])

        messages.success(request, f"BillReturn {bill_return_header.br_bill_return_no} saved successfully ✅")

        return redirect(f"/billreturn/{bill_return_header.br_rid}")

    return render(request, 'billreturn/billreturn.html', {
        'accounts': list(accounts),
        'items': list(items),
        'today': date.today(),
        'bill_return_header': bill_return_header,
        'bill_return_details': list(bill_return_details),
        'account': account
    })