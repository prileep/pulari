from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, connection
from datetime import date

from items.models import Item
from account.models import Account
from django.db.models import Value
from django.db.models.functions import Concat

from .models import SaleReturnHeader, SaleReturnDetail
from core.utils.formatter import clean_decimal

def get_next_sale_return_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_next_sequence('BillReturn')")
        row = cursor.fetchone()
    return row[0] 



def salereturn(request):

    sr_rid = request.GET.get("sr_rid")

    sale_return_header = None
    sale_return_details = []
    account = None

    # ================= CANCEL BILL =================
    if request.method == "POST" and request.POST.get("action") == "cancel":

        sr_rid = request.POST.get("sr_rid")

        SaleReturnHeader.objects.filter(sr_rid=sr_rid).update(
            sr_status="Cancelled"
        )

        messages.success(request, "SaleReturn cancelled successfully ❌")

        return redirect(f"/salereturn?sr_rid={sr_rid}")

    # ================= LOAD BILL =================
    if sr_rid:
        sale_return_header = SaleReturnHeader.objects.filter(sr_rid=sr_rid).first()
        sale_return_details = SaleReturnDetail.objects.filter(srd_sr_rid=sr_rid)

        if sale_return_header:
            account = Account.objects.get(acc_rid=sale_return_header.sr_acc_rid)

        for srd in sale_return_details:
            srd.item = Item.objects.get(item_rid=srd.srd_item_rid)

    else:
        sale_return_header = SaleReturnHeader.empty()
        saleReturn_detail = SaleReturnDetail.empty()
        sale_return_details.append(saleReturn_detail)

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

            sale_return_header = SaleReturnHeader.objects.create(
                sr_status='Active',
                sr_sale_return_no=get_next_sale_return_no(),
                   
                sr_sale_return_date=request.POST.get("sr_sale_return_date"),
                sr_notes=request.POST.get("sr_notes"),
                sr_counter_sale=request.POST.get("sr_counter_sale"),
                sr_acc_rid=request.POST.get("sr_acc_rid"),
                sr_amount=clean_decimal(request.POST.get("sr_amount") or 0),
                sr_discount=clean_decimal(request.POST.get("sr_discount") or 0),
                sr_net_amount=clean_decimal(request.POST.get("sr_net_amount") or 0),
                sr_created_date=date.today(),
                sr_modified_date=date.today()
            )

            itemRIDs = request.POST.getlist("srd_item_rid")
            quantities = request.POST.getlist("srd_qty")
            amounts = request.POST.getlist("srd_amount")
            srd_total_amounts = request.POST.getlist("srd_total_amount")
            for i in range(len(quantities)):

                qty = quantities[i]
                amt = amounts[i]

                if not qty and not amt:
                    continue

                SaleReturnDetail.objects.create(
                    srd_sr_rid=sale_return_header.sr_rid,
                    srd_item_rid=itemRIDs[i],
                    srd_qty=clean_decimal(qty),
                    srd_amount=clean_decimal(amt),
                    srd_total_amount=clean_decimal(srd_total_amounts[i])
                )

            with connection.cursor() as cursor:
                cursor.callproc('post_sale_return', [sale_return_header.sr_rid])

        messages.success(request, f"SaleReturn {sale_return_header.sr_sale_return_no} saved successfully ✅")

        return redirect(f"/salereturn?sr_rid={sale_return_header.sr_rid}")

    return render(request, 'salereturn/salereturn.html', {
        'accounts': list(accounts),
        'items': list(items),
        'today': date.today(),
        'sale_return_header': sale_return_header,
        'sale_return_details': list(sale_return_details),
        'account': account
    })