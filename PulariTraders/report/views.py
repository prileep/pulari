from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from datetime import date
from django.db.models.functions import Concat
from django.db.models import Value
from items.models import Item  # Cleaning up the duplicate broken absolute import below

def report(request):
    accounts = []
    today = date.today()

    items = Item.objects.annotate(
        display_name=Concat('item_name', Value(' - '), 'item_code')
    ).values(
        'display_name',
        'item_name',
        'item_code',
        'item_sale_price',
        'item_rid',
        'item_stk'
    )

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                acc_rid,
                acc_disp_name,
                acc_address,
                acc_phone,
                acc_code
            FROM account
            ORDER BY acc_disp_name
        """)
        rows = cursor.fetchall()

    for row in rows:
        accounts.append({
            "acc_rid": row[0],
            "acc_disp_name": row[1],
            "acc_address": row[2],
            "acc_phone": row[3],
            "acc_code": row[4],
        })

    return render(request, "report/report.html", {
        'accounts': list(accounts),
        'items': list(items),
        "today": today,
    })


def generate_report(request):
    report_name = request.GET.get("report_name", "").strip()
    
    tran_from_date = request.GET.get("tran_from_date", "").strip() or None
    tran_to_date = request.GET.get("tran_to_date", "").strip() or None
    
    try:
        tran_item_rid = int(request.GET.get("tran_item_rid", "").strip() or 0)
    except ValueError:
        tran_item_rid = 0

    try:
        tran_account_rid = int(request.GET.get("tran_account_rid", "").strip() or 0)
    except ValueError:
        tran_account_rid = 0

    acctran_ref_type = request.GET.get("acctran_ref_type", "").strip() or None

    params = [
        tran_from_date,
        tran_to_date,
        tran_item_rid,
        tran_account_rid,
        acctran_ref_type
    ]

    details = []

    if report_name == "Stock Transaction":
        with connection.cursor() as curStockTransaction:
            curStockTransaction.callproc('stock_transaction_report', params)
            
            if curStockTransaction.description:
                columns = [col[0] for col in curStockTransaction.description]
                rows = [dict(zip(columns, row)) for row in curStockTransaction.fetchall()]
            else:
                rows = []

        # OPTIMIZATION: Sorting by item_code first allows your JS structure to build sequential sections easily,
        # while keeping our primary structural ordering intact.
        rows.sort(key=lambda x: (x.get("item_code") or ""))

        for i, row in enumerate(rows, start=1):
            t_date = row.get("trans_date")
            formatted_date = t_date.strftime("%d-%m-%Y") if hasattr(t_date, "strftime") else str(t_date or "")

            details.append({
                "slno": i,
                "trans_date": formatted_date,
                "acc_disp_name": row.get("acc_disp_name") or "",
                "acctran_ref_type": row.get("acctran_ref_type") or "",
                "item_name": row.get("item_name") or "",
                "item_code": row.get("item_code") or "",
                "stock_in": int(row.get("stock_in") or 0),
                "stock_out": int(row.get("stock_out") or 0),
                "item_amt": float(row.get("item_amt") or 0),
                "item_tot_amt": float(row.get("item_tot_amt") or 0)
            })

    return JsonResponse({
        "report_type": report_name,
        "details": details,
    })