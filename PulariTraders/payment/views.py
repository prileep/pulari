from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date
from django.utils import timezone  # Standard utility for Django tracking

from account.models import Account
from django.db.models import Value
from django.db.models.functions import Concat

from .models import Payment
from core.utils.formatter import clean_decimal

def get_next_payment_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_next_sequence('Payment')")
        row = cursor.fetchone()
    return row[0]


def payment(request, rid=None):

    if not rid:
        rid = request.GET.get("pay_rid")

    payment = None
    account = None

    # ================= CANCEL BILL =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        with transaction.atomic():

            rid = request.POST.get("rid")

            payment = Payment.objects.filter(pay_rid=rid).first();
            if payment and payment.pay_status != "Cancelled":
                payment.pay_status = "Cancelled"
                payment.pay_modified_date = timezone.now()
                payment.save()

                with connection.cursor() as cursor:
                    cursor.callproc('post_payment', [payment.pay_rid])

        messages.success(request, "Payment cancelled successfully ❌")
        
        return redirect(f"/payment/{rid}")

    # ================= LOAD BILL =================
    if rid:
        payment = Payment.objects.filter(pay_rid=rid).first()

        if payment:
            account = Account.objects.get(acc_rid=payment.pay_acc_rid)

    else:
        payment = Payment.empty()

    accounts = Account.objects.filter().values(
        'acc_rid', 'acc_disp_name', 'acc_name',
        'acc_place', 'acc_phone', 'acc_address', 'acc_code'
    )

    # ================= SAVE BILL =================
    if request.method == "POST":

        with transaction.atomic():
            
            payment = Payment.objects.create(
                pay_status='Active',
                pay_no=get_next_payment_no(),
                pay_date=request.POST.get("pay_date"),
                pay_amt=clean_decimal(request.POST.get("pay_amt") or 0),
                pay_acc_rid=request.POST.get("pay_acc_rid"),
                pay_notes=request.POST.get("pay_notes"),
                pay_created_date=timezone.now(),
                pay_modified_date=timezone.now()
            )

            with connection.cursor() as cursor:
                cursor.callproc('post_payment', [payment.pay_rid])

        messages.success(request, f"Payment {payment.pay_no} saved successfully ✅")

        return redirect(f"/payment?pay_rid={payment.pay_rid}")

    return render(request, 'payment/payment.html', {
        'accounts': list(accounts),
        'today': date.today(),
        'payment': payment,
        'account': account
    })