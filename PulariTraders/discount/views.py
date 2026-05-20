from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date

from account.models import Account
from django.db.models import Value
from django.db.models.functions import Concat

from .models import Discount
from core.utils.formatter import clean_decimal

def get_next_discount_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_next_sequence('Discount')")
        row = cursor.fetchone()
    return row[0]


def discount(request, rid=None):

    disc_rid = request.GET.get("disc_rid") or rid

    discount = None
    account = None

    # ================= CANCEL BILL =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        with transaction.atomic():

            disc_rid = request.POST.get("disc_rid")

            Discount.objects.filter(disc_rid=disc_rid).update(
                disc_status="Cancelled"
            )

            with connection.cursor() as cursor:
                cursor.callproc('post_discount', [discount.disc_rid])

        messages.success(request, "Discount cancelled successfully ❌")

        return redirect(f"/discount?disc_rid={disc_rid}")

    # ================= LOAD BILL =================
    if disc_rid:
        discount = Discount.objects.filter(disc_rid=disc_rid).first()

        if discount:
            account = Account.objects.get(acc_rid=discount.disc_acc_rid)

    else:
        discount = Discount.empty()

    accounts = Account.objects.filter().values(
        'acc_rid', 'acc_disp_name', 'acc_name',
        'acc_place', 'acc_phone', 'acc_address', 'acc_code'
    )

    # ================= SAVE BILL =================
    if request.method == "POST":

        with transaction.atomic():

            discount = Discount.objects.create(
                disc_status='Active',
                disc_no=get_next_discount_no(),
                disc_date=request.POST.get("disc_date"),
                disc_amt=clean_decimal(request.POST.get("disc_amt") or 0),
                disc_acc_rid=request.POST.get("disc_acc_rid"),
                disc_notes=request.POST.get("disc_notes"),
                disc_created_date=date.today(),
                disc_modified_date=date.today()
            )

            with connection.cursor() as cursor:
                cursor.callproc('post_discount', [discount.disc_rid])

        messages.success(request, f"Discount {discount.disc_no} saved successfully ✅")

        return redirect(f"/discount?disc_rid={discount.disc_rid}")

    return render(request, 'discount/discount.html', {
        'accounts': list(accounts),
        'today': date.today(),
        'discount': discount,
        'account': account
    })