from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date

from account.models import Account
from django.db.models import Value
from django.db.models.functions import Concat

from .models import Receipt
from core.utils.formatter import clean_decimal

def get_next_receipt_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_next_sequence('Receipt')")
        row = cursor.fetchone()
    return row[0]


def receipt(request, rid=None):
    if not rid:
        rid = request.GET.get("rid")

    receipt_obj = None
    account = None

    # ================= CANCEL RECEIPT =================
    if request.method == "POST" and request.POST.get("action") == "cancel":
        with transaction.atomic():
            rid = request.POST.get("rid")
            receipt_obj = Receipt.objects.filter(rcpt_rid=rid).first()

            if receipt_obj and receipt_obj.rcpt_status != "Cancelled":
                receipt_obj.rcpt_status = "Cancelled"
                receipt_obj.save()

                with connection.cursor() as cursor:
                    cursor.callproc('post_receipt', [receipt_obj.rcpt_rid])

        messages.success(request, "Receipt cancelled successfully ❌")
        return redirect(f"/receipt/{rid}/")

    # ================= SAVE RECEIPT =================
    elif request.method == "POST":
        with transaction.atomic():
            receipt_obj = Receipt.objects.create(
                rcpt_status='Active',
                rcpt_no=get_next_receipt_no(),
                rcpt_date=request.POST.get("rcpt_date"),
                rcpt_amt=clean_decimal(request.POST.get("rcpt_amt") or 0),
                rcpt_acc_rid=int(request.POST.get("rcpt_acc_rid") or 0),
                rcpt_notes=request.POST.get("rcpt_notes"),
                rcpt_created_date=date.today(),
                rcpt_modified_date=date.today()
            )

            with connection.cursor() as cursor:
                cursor.callproc('post_receipt', [receipt_obj.rcpt_rid])

        messages.success(request, f"Receipt {receipt_obj.rcpt_no} saved successfully ✅")
        return redirect(f"/receipt/{receipt_obj.rcpt_rid}/")

    # ================= LOAD RECEIPT (GET) =================
    if rid:
        receipt_obj = Receipt.objects.filter(rcpt_rid=rid).first()

        if receipt_obj:
            account = Account.objects.get(acc_rid=receipt_obj.rcpt_acc_rid)
    else:
        receipt_obj = Receipt.empty()

    accounts = Account.objects.filter().values(
        'acc_rid', 'acc_disp_name', 'acc_name',
        'acc_place', 'acc_phone', 'acc_address', 'acc_code'
    )

    return render(request, 'receipt/receipt.html', {
        'accounts': list(accounts),
        'today': date.today(),
        'receipt': receipt_obj,
        'account': account
    })