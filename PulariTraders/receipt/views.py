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


def receipt(request):

    rcpt_rid = request.GET.get("rcpt_rid")

    receipt = None
    account = None

    # ================= CANCEL BILL =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        rcpt_rid = request.POST.get("rcpt_rid")

        Receipt.objects.filter(rcpt_rid=rcpt_rid).update(
            rcpt_status="Cancelled"
        )

        messages.success(request, "Receipt cancelled successfully ❌")

        return redirect(f"/receipt?rcpt_rid={rcpt_rid}")

    # ================= LOAD BILL =================
    if rcpt_rid:
        receipt = Receipt.objects.filter(rcpt_rid=rcpt_rid).first()

        if receipt:
            account = Account.objects.get(acc_rid=receipt.rcpt_acc_rid)

    else:
        receipt = Receipt.empty()

    accounts = Account.objects.filter().values(
        'acc_rid', 'acc_disp_name', 'acc_name',
        'acc_place', 'acc_phone', 'acc_address', 'acc_code'
    )

    # ================= SAVE BILL =================
    if request.method == "POST":

        with transaction.atomic():

            receipt = Receipt.objects.create(
                rcpt_status='Active',
                rcpt_no=get_next_receipt_no(),
                rcpt_date=request.POST.get("rcpt_date"),
                rcpt_amt=clean_decimal(request.POST.get("rcpt_amt") or 0),
                rcpt_acc_rid=request.POST.get("rcpt_acc_rid"),
                rcpt_notes=request.POST.get("rcpt_notes"),
                rcpt_created_date=date.today(),
                rcpt_modified_date=date.today()
            )

            with connection.cursor() as cursor:
                cursor.callproc('post_receipt', [receipt.rcpt_rid])

        messages.success(request, f"Receipt {receipt.rcpt_no} saved successfully ✅")

        return redirect(f"/receipt?rcpt_rid={receipt.rcpt_rid}")

    return render(request, 'receipt/receipt.html', {
        'accounts': list(accounts),
        'today': date.today(),
        'receipt': receipt,
        'account': account
    })