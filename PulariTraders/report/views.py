from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import connection
from datetime import date
from django.db.models.functions import Concat
from django.db.models import Value
from items.models import Item
from account.models import Account

def report(request):
    accounts = []
    items = []
    today = date.today()

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

    return render(request, "report/report.html", {
        'accounts': list(accounts),
        'items': list(items),
        "today": today,
    })

def printreport(request):
    report_name = request.POST.get("report_name", "").strip()
    
    tran_from_date = request.POST.get("tran_from_date", "").strip() or None
    tran_to_date = request.POST.get("tran_to_date", "").strip() or None
    tran_account_rid = int(request.POST.get("tran_account_rid") or 0)
    tran_item_rid = int(request.POST.get("tran_item_rid") or 0) 
    acctran_ref_type = request.POST.get("acctran_ref_type", "").strip() or None

    params = []
    
    if report_name == "Stock Transaction":
        params = [
            tran_from_date,
            tran_to_date,
            tran_item_rid,
            tran_account_rid,
            acctran_ref_type
        ]
        details = _stock_transaction_report(request, params)

        context = {
            "tran_from_date": tran_from_date,
            "tran_to_date": tran_to_date,
            "report_type": report_name,
            "details": details,
        }
        return render(request, "report/stock_transaction_report.html", context)

    if report_name == "Account Transaction":
        rows = []
        params = [
            acctran_ref_type,
            tran_from_date,
            tran_to_date,
            tran_account_rid
        ]
        
        with connection.cursor() as cursor:
            cursor.callproc('account_transaction_report', params)
            columns = [col[0] for col in cursor.description]
            search_rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for i, row in enumerate(search_rows, start=1):
            acctran_date = row["acctran_date"]

            rows.append({
                "slno": i,
                "acctran_date": acctran_date.strftime("%d-%m-%Y") if acctran_date else "",
                "acctran_ref_type": row["acctran_ref_type"] or "",
                "acctran_ref_rid": row["acctran_ref_rid"] or "",
                "acctran_ref_no": row["acctran_ref_no"] or "",
                "acc_notes": row["acc_notes"] or "",
                "acc_name": row["acc_name"] or "",
                "acctran_status": row["acctran_status"] or "",
                "cr_amt": int(row["cr_amt"] or 0),
                "dr_amt": int(row["dr_amt"] or 0),
                "balance": int(row["balance"] or 0),
                "open_balance": int(row["open_balance"] or 0),
                "closing_balance": int(row["closing_balance"] or 0)
            })
            
        # Create a separate sorted list exclusively for the summary pivot matrix,
        # leaving the original 'rows' in their exact procedure execution order.
        pivot_rows = sorted(rows, key=lambda x: (x.get("acctran_ref_type") or ""))

        params = [
            tran_from_date,
            tran_to_date,
            tran_item_rid,
            tran_account_rid,
            acctran_ref_type
        ]
        stockTrans = _stock_transaction_report(request, params)

        tran_account_name = "All Accounts"
        if(tran_account_rid > 0):
            account = Account.objects.filter(acc_rid=tran_account_rid).first()
            if account:
                tran_account_name = account.acc_disp_name
            else:
                tran_account_name = "Unknown Account" 

        opening_balance = 0;
        closing_balance = 0;
        if rows and len(rows) > 0:
            opening_balance = int(rows[0].get("open_balance", 0))
            closing_balance = int(rows[0].get("closing_balance", 0))

        context = {
            "tran_from_date": tran_from_date,
            "tran_to_date": tran_to_date,
            "report_type": report_name,
            "rows": rows,
            "pivot_rows": pivot_rows,
            "stockTrans": stockTrans,
            "tran_account_rid": tran_account_rid,
            "tran_account_name": tran_account_name,
            "opening_balance": int(opening_balance),
            "closing_balance": closing_balance,
        }
        return render(request, "report/account_transaction_report.html", context)

    return redirect('report')

def _stock_transaction_report(request, params):
    details = []
    
    with connection.cursor() as curStockTransaction:
        curStockTransaction.callproc('stock_transaction_report', params)
        
        if curStockTransaction.description:
            columns = [col[0] for col in curStockTransaction.description]
            rows = [dict(zip(columns, row)) for row in curStockTransaction.fetchall()]
        else:
            rows = []

    rows.sort(key=lambda x: (x.get("item_code") or ""))

    details = []  
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

    return details