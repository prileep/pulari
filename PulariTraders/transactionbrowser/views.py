from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from datetime import date

def transaction_browser(request):
	accounts = []
	today = date.today()

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

	return render(request, "transactionbrowser/transactionbrowser.html", {
		'accounts': list(accounts),
		"today": today,
	})


def transaction_search(request):
	acctran_ref_type = request.GET.get("acctran_ref_type", "").strip() or None
	status = request.GET.get("status", "").strip() or None
	from_date = request.GET.get("from_date", "").strip() or None
	to_date = request.GET.get("to_date", "").strip() or None
	account_rid = request.GET.get("account_rid", "").strip() or None
	refno = request.GET.get("refno", "").strip() or None
	notes = request.GET.get("notes", "").strip() or None
	amount_from = request.GET.get("amount_from", "").strip() or None
	amount_to = request.GET.get("amount_to", "").strip() or None

	params = [
		acctran_ref_type,
		status,
		from_date,
		to_date,
		int(account_rid) if account_rid else None,
		refno,
		notes,
		amount_from if amount_from else None,
		amount_to if amount_to else None,
	]

	transactions = []
	itemsummary = []

	# Isolation Context Block 1: Main Transaction Ledger Search
	with connection.cursor() as cursor:
		cursor.callproc('sp_transaction_search', params)
		columns = [col[0] for col in cursor.description]
		search_rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

	for i, row in enumerate(search_rows, start=1):
		acctran_date = row["acctran_date"]

		transactions.append({
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
			"open_balance": int(row["open_balance"] or 0)
		})
		
	# Isolation Context Block 2: Second call to same procedure with separate cursor stream
	with connection.cursor() as curItemSummary:
		curItemSummary.callproc('sp_balance_sheet_item_summary', params)
		if curItemSummary.description:
			summary_columns = [col[0] for col in curItemSummary.description]
			summary_rows = [dict(zip(summary_columns, row)) for row in curItemSummary.fetchall()]
		else:
			summary_rows = []

	for i, row in enumerate(summary_rows, start=1):
		# Safe fallback evaluation to align transaction keys into expected itemsummary keys
		itemsummary.append({
			"item_name": row.get("acc_name") or row.get("item_name") or "",
			"item_code": row.get("acctran_ref_no") or row.get("item_code") or "",
			"StockIn": int(row.get("dr_amt") or row.get("StockIn") or 0),
			"StockOut": int(row.get("cr_amt") or row.get("StockOut") or 0)
		})

	return JsonResponse({
		"mode": "account" if account_rid else "general",
		"transactions": transactions,
		"itemsummary": itemsummary
	})