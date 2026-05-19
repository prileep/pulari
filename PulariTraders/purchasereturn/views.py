from django.shortcuts import render

# def purchase_return(request):
#     return render(request, 'purchasereturn/purchasereturn.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date

from items.models import Item
from account.models import Account
from django.db.models import Value
from django.db.models.functions import Concat

from .models import PurchasereturnHeader,PurchasereturnDetail
from core.utils.formatter import clean_decimal

def get_next_purchase_return_no():
    with connection.cursor() as cursor:
        # cursor.execute("SELECT get_next_purchase_return_no('PurchaseReturn')")
        cursor.execute("SELECT get_next_sequence('PurchaseReturn')")
        row = cursor.fetchone()
    return row[0]

def purchasereturn(request):

    pr_rid = request.GET.get("pr_rid")

    purchase_return_header = None
    purchase_return_details = []
    account = None

    # ================= CANCEL BILL =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        pr_rid = request.POST.get("pr_rid")

        PurchasereturnHeader.objects.filter(pr_rid=pr_rid).update(
            pr_status="Cancelled"
        )

        messages.success(request, "PurchaseReturn cancelled successfully ❌")

        return redirect(f"/purchaseReturn?pr_rid={pr_rid}")

    # ================= LOAD BILL =================
    if pr_rid:
        purchase_return_header = PurchasereturnHeader.objects.filter(pr_rid=pr_rid).first()
        purchase_return_details = PurchasereturnDetail.objects.filter(prd_pr_rid=pr_rid)

        if purchase_return_header:
            account = Account.objects.get(acc_rid=purchase_return_header.pr_acc_rid)

        for prd in purchase_return_details:
            prd.item = Item.objects.get(item_rid=prd.prd_item_rid)

    else:
        purchase_return_header = PurchasereturnHeader.empty()
        purchaseReturn_detail = PurchasereturnDetail.empty()
        purchase_return_details.append(purchaseReturn_detail)

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

            purchase_return_header = PurchasereturnHeader.objects.create(
                pr_status='Active',
                pr_purchase_return_no=get_next_purchase_return_no(),
                
                pr_purchase_return_date=request.POST.get("pr_purchase_return_date"),
                pr_notes=request.POST.get("pr_notes"),
                pr_counter_purchase=request.POST.get("pr_counter_purchase"),
                pr_acc_rid=request.POST.get("pr_acc_rid"),
                pr_amount=clean_decimal(request.POST.get("pr_amount") or 0),
                pr_discount=clean_decimal(request.POST.get("pr_discount") or 0),
                pr_net_amount=clean_decimal(request.POST.get("pr_net_amount") or 0),
                pr_created_date=date.today(),
                pr_modified_date=date.today()
            )

            itemRIDs = request.POST.getlist("prd_item_rid")
            quantities = request.POST.getlist("prd_qty")
            amounts = request.POST.getlist("prd_amount")
            prd_total_amounts = request.POST.getlist("prd_total_amount")
            for i in range(len(quantities)):

                qty = quantities[i]
                amt = amounts[i]

                if not qty and not amt:
                    continue

                PurchasereturnDetail.objects.create(
                    prd_pr_rid=purchase_return_header.pr_rid,
                    prd_item_rid=itemRIDs[i],
                    prd_qty=clean_decimal(qty),
                    prd_amount=clean_decimal(amt),
                    prd_total_amount=clean_decimal(prd_total_amounts[i])
                )

            with connection.cursor() as cursor:
                cursor.callproc('post_purchase_return', [purchase_return_header.pr_rid])

        messages.success(request, f"PurchaseReturn {purchase_return_header.pr_purchase_return_no} saved successfully ✅")

        return redirect(f"/purchasereturn?pr_rid={purchase_return_header.pr_rid}")

    return render(request, 'purchasereturn/purchasereturn.html', {
        'accounts': list(accounts),
        'items': list(items),
        'today': date.today(),
        'purchase_return_header': purchase_return_header,
        'purchase_return_details': list(purchase_return_details),
        'account': account
    })