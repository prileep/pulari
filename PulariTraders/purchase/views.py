from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date

from items.models import Item
from account.models import Account
from django.db.models import Value
from django.db.models.functions import Concat

from .models import PurchaseHeader, PurchaseDetail
from core.utils.formatter import clean_decimal


def get_next_purchase_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_next_sequence('Purchase')")
        row = cursor.fetchone()
    return row[0]


def printpurchase(request, rid):

    purchase_header = PurchaseHeader.objects.filter(
        ph_rid=rid
    ).first()

    purchase_details = PurchaseDetail.objects.filter(
        pd_ph_rid=rid
    )

    account = None

    if purchase_header:
        account = Account.objects.filter(
            acc_rid=purchase_header.ph_acc_rid
        ).first()

    for pd in purchase_details:
        pd.item = Item.objects.get(
            item_rid=pd.pd_item_rid
        )

    return render(request, 'purchase/printpurchase.html', {
        'purchase_header': purchase_header,
        'purchase_details': purchase_details,
        'account': account
    })


def purchase(request, rid=None):

    if not rid:
        rid = request.GET.get("rid")

    purchase_header = None
    purchase_details = []
    account = None

    # ================= CANCEL PURCHASE =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        with transaction.atomic():
            
            rid = request.POST.get("rid")
            purchase_header = PurchaseHeader.objects.filter(ph_rid=rid).first()

            if purchase_header: # Good practice to check for None
                purchase_header.ph_status = "Cancelled"
                purchase_header.save() # This works!

                with connection.cursor() as cursor:
                        cursor.callproc('post_purchase', [purchase_header.ph_rid])

        messages.success(request, "Purchase cancelled successfully ❌")

        return redirect(f"/purchase/{rid}/")

    # ================= LOAD PURCHASE =================
    if rid:
        purchase_header = PurchaseHeader.objects.filter(ph_rid=rid).first()
        purchase_details = PurchaseDetail.objects.filter(pd_ph_rid=rid)

        if purchase_header:
            account = Account.objects.get(acc_rid=purchase_header.ph_acc_rid)

        for pd in purchase_details:
            pd.item = Item.objects.get(item_rid=pd.pd_item_rid)

    else:
        purchase_header = PurchaseHeader.empty()
        purchase_detail = PurchaseDetail.empty()
        purchase_details.append(purchase_detail)

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

    # ================= SAVE PURCHASE =================
    if request.method == "POST":

        with transaction.atomic():

            purchase_header = PurchaseHeader.objects.create(
                ph_status='Active',
                ph_purchase_no=get_next_purchase_no(),
                ph_purchase_date=request.POST.get("ph_purchase_date"),
                ph_notes=request.POST.get("ph_notes"),
                ph_counter_sale=request.POST.get("ph_counter_sale"),
                ph_acc_rid=request.POST.get("ph_acc_rid"),
                ph_amount=clean_decimal(request.POST.get("ph_amount") or 0),
                ph_discount=clean_decimal(request.POST.get("ph_discount") or 0),
                ph_net_amount=clean_decimal(request.POST.get("ph_net_amount") or 0),
                ph_created_date=date.today(),
                ph_modified_date=date.today()
            )

            itemRIDs = request.POST.getlist("pd_item_rid")
            quantities = request.POST.getlist("pd_qty")
            amounts = request.POST.getlist("pd_amount")
            pd_total_amounts = request.POST.getlist("pd_total_amount")
            for i in range(len(quantities)):

                qty = quantities[i]
                amt = amounts[i]

                if not qty and not amt:
                    continue

                PurchaseDetail.objects.create(
                    pd_ph_rid=purchase_header.ph_rid,
                    pd_item_rid=itemRIDs[i],
                    pd_qty=clean_decimal(qty),
                    pd_amount=clean_decimal(amt),
                    pd_total_amount=clean_decimal(pd_total_amounts[i])
                )

            with connection.cursor() as cursor:
                cursor.callproc('post_purchase', [purchase_header.ph_rid])

        messages.success(request, f"Purchase {purchase_header.ph_purchase_no} saved successfully ✅")

        return redirect(f"/purchase?ph_rid={purchase_header.ph_rid}")

    return render(request, 'purchase/purchase.html', {
        'accounts': list(accounts),
        'items': list(items),
        'today': date.today(),
        'purchase_header': purchase_header,
        'purchase_details': list(purchase_details),
        'account': account
    })