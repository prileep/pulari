from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date
from django.utils import timezone  # Standard utility for Django tracking

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

    if not rid:
        rid = request.GET.get("rid")

    discount = None
    account = None

    # ================= CANCEL BILL =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        with transaction.atomic():

            rid = request.POST.get("rid")

            discount_obj = Discount.objects.filter(disc_rid=rid).first();

            if discount_obj and discount_obj.disc_status != "Cancelled":
                discount_obj.disc_status = "Cancelled"
                discount_obj.disc_modified_date = timezone.now()
                discount_obj.save()

                with connection.cursor() as cursor:
                    cursor.callproc('post_discount', [discount_obj.disc_rid])

        messages.success(request, "Discount cancelled successfully ❌")
        return redirect(f"/discount/{rid}/")
    
    # ================= SAVE BILL =================
    elif request.method == "POST":

        with transaction.atomic():

            discount = Discount.objects.create(
                disc_status='Active',
                disc_no=get_next_discount_no(),
                disc_date=request.POST.get("disc_date"),
                disc_amt=clean_decimal(request.POST.get("disc_amt") or 0),
                disc_acc_rid=request.POST.get("disc_acc_rid"),
                disc_notes=request.POST.get("disc_notes"),
                disc_created_date=timezone.now(),
                disc_modified_date=timezone.now()
            )

            with connection.cursor() as cursor:
                cursor.callproc('post_discount', [discount.disc_rid])

        messages.success(request, f"Discount {discount.disc_no} saved successfully ✅")

        return redirect(f"/discount/{discount.disc_rid}/")

    # ================= LOAD DISCOUNT =================
    if rid:
        discount = Discount.objects.filter(disc_rid=rid).first()

        if discount:
            account = Account.objects.get(acc_rid=discount.disc_acc_rid)

    else:
        discount = Discount.empty()

    accounts = Account.objects.filter().values(
        'acc_rid', 'acc_disp_name', 'acc_name',
        'acc_place', 'acc_phone', 'acc_address', 'acc_code'
    )

    

    return render(request, 'discount/discount.html', {
        'accounts': list(accounts),
        'today': date.today(),
        'discount': discount,
        'account': account
    })