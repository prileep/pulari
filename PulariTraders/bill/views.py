from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date

from items.models import Item
from account.models import Account
from django.db.models import Value
from django.db.models.functions import Concat

from .models import BillHeader, BillDetail
from core.utils.formatter import clean_decimal


def get_next_bill_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_next_sequence('Bill')")
        row = cursor.fetchone()
    return row[0]

def printbill(request, rid):

    bill_header = BillHeader.objects.filter(
        bh_rid=rid
    ).first()

    bill_details = BillDetail.objects.filter(
        bd_bh_rid=rid
    )

    account = None

    if bill_header:
        account = Account.objects.filter(
            acc_rid=bill_header.bh_acc_rid
        ).first()

    for bd in bill_details:
        bd.item = Item.objects.get(
            item_rid=bd.bd_item_rid
        )

    return render(request, 'bill/printbill.html', {
        'bill_header': bill_header,
        'bill_details': bill_details,
        'account': account
    })


def bill(request, rid=None):

    if not rid:
        rid = request.GET.get("rid")

    bill_header = None
    bill_details = []
    account = None

    # ================= CANCEL BILL =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        with transaction.atomic():
            
            rid = request.POST.get("rid")
            bill_header = BillHeader.objects.filter(bh_rid=rid).first()

            if bill_header: # Good practice to check for None
                bill_header.bh_status = "Cancelled"
                bill_header.save() # This works!

                with connection.cursor() as cursor:
                        cursor.callproc('post_bill', [bill_header.bh_rid])

        messages.success(request, "Bill cancelled successfully ❌")

        return redirect(f"/bill/{rid}/")

    # ================= LOAD BILL =================
    if rid:
        bill_header = BillHeader.objects.filter(bh_rid=rid).first()
        bill_details = BillDetail.objects.filter(bd_bh_rid=rid)

        if bill_header:
            account = Account.objects.get(acc_rid=bill_header.bh_acc_rid)

        for bd in bill_details:
            bd.item = Item.objects.get(item_rid=bd.bd_item_rid)

    else:
        bill_header = BillHeader.empty()
        bill_detail = BillDetail.empty()
        bill_details.append(bill_detail)

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

            bill_header = BillHeader.objects.create(
                bh_status='Active',
                bh_bill_no=get_next_bill_no(),
                bh_bill_date=request.POST.get("bh_bill_date"),
                bh_notes=request.POST.get("bh_notes"),
                bh_counter_sale=request.POST.get("bh_counter_sale"),
                bh_acc_rid=request.POST.get("bh_acc_rid"),
                bh_amount=clean_decimal(request.POST.get("bh_amount") or 0),
                bh_discount=clean_decimal(request.POST.get("bh_discount") or 0),
                bh_net_amount=clean_decimal(request.POST.get("bh_net_amount") or 0),
                bh_created_date=date.today(),
                bh_modified_date=date.today()
            )

            itemRIDs = request.POST.getlist("bd_item_rid")
            quantities = request.POST.getlist("bd_qty")
            amounts = request.POST.getlist("bd_amount")
            bd_total_amounts = request.POST.getlist("bd_total_amount")
            for i in range(len(quantities)):

                qty = quantities[i]
                amt = amounts[i]

                if not qty and not amt:
                    continue

                BillDetail.objects.create(
                    bd_bh_rid=bill_header.bh_rid,
                    bd_item_rid=itemRIDs[i],
                    bd_qty=clean_decimal(qty),
                    bd_amount=clean_decimal(amt),
                    bd_total_amount=clean_decimal(bd_total_amounts[i])
                )

            with connection.cursor() as cursor:
                cursor.callproc('post_bill', [bill_header.bh_rid])

        messages.success(request, f"Bill {bill_header.bh_bill_no} saved successfully ✅")

        return redirect(f"/bill/{bill_header.bh_rid}/")

    return render(request, 'bill/bill.html', {
        'accounts': list(accounts),
        'items': list(items),
        'today': date.today(),
        'bill_header': bill_header,
        'bill_details': list(bill_details),
        'account': account
    })