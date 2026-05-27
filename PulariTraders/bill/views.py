from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date
from django.utils import timezone  # Standard utility for Django tracking

from receipt.models import Receipt
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


def get_next_receipt_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_next_sequence('Receipt')")
        row = cursor.fetchone()
    return row[0]


def printbill(request, rid):
    bill_header = BillHeader.objects.filter(bh_rid=rid).first()
    bill_details = BillDetail.objects.filter(bd_bh_rid=rid)
    account = None

    if bill_header:
        account = Account.objects.filter(acc_rid=bill_header.bh_acc_rid).first()

    for bd in bill_details:
        bd.item = Item.objects.get(item_rid=bd.bd_item_rid)

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

            if bill_header and bill_header.bh_status != "Cancelled":
                bill_header.bh_status = "Cancelled"
                bill_header.bh_modified_date = timezone.now()
                bill_header.save()

                with connection.cursor() as cursor:
                    cursor.callproc('post_bill', [bill_header.bh_rid])

                if bill_header.bh_rcpt_rid and bill_header.bh_rcpt_rid > 0:
                    receipt = Receipt.objects.filter(rcpt_rid=bill_header.bh_rcpt_rid).first()
                    if receipt:
                        receipt.rcpt_status = "Cancelled"
                        receipt.save()
        
                        with connection.cursor() as cursor:
                            cursor.callproc('post_receipt', [receipt.rcpt_rid])

        messages.success(request, "Bill cancelled successfully ❌")
        return redirect(f"/bill/{rid}/")

    # ================= SAVE BILL =================
    elif request.method == "POST":
        with transaction.atomic():

            bill_header = BillHeader.objects.create(
                bh_status='Active',
                bh_bill_no=get_next_bill_no(),
                bh_bill_date=request.POST.get("bh_bill_date"),
                bh_notes=request.POST.get("bh_notes"),
                bh_counter_sale=int(request.POST.get("bh_counter_sale") or 0),
                bh_acc_rid=int(request.POST.get("bh_acc_rid") or 0),
                bh_amount=clean_decimal(request.POST.get("bh_amount") or 0),
                bh_discount=clean_decimal(request.POST.get("bh_discount") or 0),
                bh_net_amount=clean_decimal(request.POST.get("bh_net_amount") or 0),
                bh_created_date=timezone.now(),
                bh_modified_date=timezone.now()
            )

            bd_item_rid = request.POST.getlist("bd_item_rid")
            bd_qty = request.POST.getlist("bd_qty")
            bd_amount = request.POST.getlist("bd_amount")
            bd_total_amount = request.POST.getlist("bd_total_amount")
            
            for i in range(len(bd_qty)):
                
                if not bd_qty[i] and not bd_amount[i]:
                    continue

                BillDetail.objects.create(
                    bd_bh_rid=bill_header.bh_rid,
                    bd_item_rid=bd_item_rid[i],
                    bd_qty=clean_decimal(bd_qty[i]),
                    bd_amount=clean_decimal(bd_amount[i]),
                    bd_total_amount=clean_decimal(bd_total_amount[i])
                )

            with connection.cursor() as cursor:
                cursor.callproc('post_bill', [bill_header.bh_rid])

            if bill_header.bh_counter_sale == 1:
                receipt = Receipt.objects.create(
                    rcpt_status="Active",
                    rcpt_no=get_next_receipt_no(),
                    rcpt_date=bill_header.bh_bill_date,
                    rcpt_amt=bill_header.bh_net_amount,
                    rcpt_acc_rid=bill_header.bh_acc_rid,
                    rcpt_notes=f"CASH PARTY {bill_header.bh_bill_no}",
                    rcpt_created_date=timezone.now(),
                    rcpt_modified_date=timezone.now()
                )

                with connection.cursor() as cursor:
                    cursor.callproc('post_receipt', [receipt.rcpt_rid])
                
                # Link the newly created receipt back into the bill header tracker
                bill_header.bh_rcpt_rid = receipt.rcpt_rid
                bill_header.save()

        messages.success(request, f"Bill {bill_header.bh_bill_no} saved successfully ✅")
        return redirect(f"/bill/{bill_header.bh_rid}/")

    # ================= LOAD BILL (GET) =================
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

    return render(request, 'bill/bill.html', {
        'accounts': list(accounts),
        'items': list(items),
        'today': date.today(),
        'bill_header': bill_header,
        'bill_details': list(bill_details),
        'account': account
    })