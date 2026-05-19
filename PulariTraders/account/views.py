from urllib import request
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
# Create your views here.
from .models import *
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse

def home(request):
    return render(request, 'accounts/home.html')

def account_list(request):
    sort = request.GET.get('sort', '')

    accounts = Account.objects.all()

    # ✅ Allow only valid fields (security)
    allowed_fields = ['acc_code', 'acc_name', 'acc_place', 'acc_phone']

    if sort:
        field = sort.replace('-', '')
        if field in allowed_fields:
            accounts = account.order_by(sort)

    return render(request, 'accounts/account_list.html', {
        'accounts': accounts,
        'current_sort': sort
    })

import re

def account(request, pk):

    account_obj = None

    if pk != 0:
        account_obj = get_object_or_404(Account, acc_rid=pk)

    if pk == 0:
        last_account = Account.objects.order_by('-acc_rid').first()

        if last_account and last_account.acc_code:
            match = re.search(r'\d+', last_account.acc_code)
            last_id = int(match.group()) if match else 0
        else:
            last_id = 0

        next_id = f"A{last_id + 1:04d}"
    else:
        next_id = None

    if request.method == "POST":

        def yn(field):
            return "Yes" if request.POST.get(field) == "Yes" else "No"

        is_customer = yn("acc_is_customer")
        is_supplier = yn("acc_is_supplier")
        is_staff = yn("acc_is_staff")

        try:
            if account_obj:
                account_obj.acc_name = request.POST.get("acc_name")
                account_obj.acc_place = request.POST.get("acc_place")
                account_obj.acc_phone = request.POST.get("acc_phone")
                account_obj.acc_address = request.POST.get("acc_address")

                account_obj.acc_is_customer = is_customer
                account_obj.acc_is_supplier = is_supplier
                account_obj.acc_is_staff = is_staff

                account_obj.save()

                messages.success(request, "Account updated successfully")
                

            else:
                Account.objects.create(
                    acc_code=request.POST.get("acc_code"),
                    acc_name=request.POST.get("acc_name"),
                    acc_place=request.POST.get("acc_place"),
                    acc_phone=request.POST.get("acc_phone"),
                    acc_address=request.POST.get("acc_address"),

                    acc_is_customer=is_customer,
                    acc_is_supplier=is_supplier,
                    acc_is_staff=is_staff,
                )

                messages.success(request, "Account created successfully")
                account_obj = None

        except IntegrityError:
            messages.error(request, "❌ Name and Place already exists!")

        # return redirect('account_list')

    return render(request, 'accounts/account.html', {
        'account': account_obj,
        'next_id': next_id
    })
def search_customer(request):
    query = request.GET.get('q', '')

    customers = Account.objects.filter(
        acc_is_customer=True,
        acc_name__istartswith=query
    )

    data = list(customers.values('acc_rid', 'acc_name'))

    return JsonResponse(data, safe=False)

def purchase_list(request):
    return HttpResponse("Purchase Module")

def receipt_list(request):
    return HttpResponse("Receipt Module")

def transaction_list(request):
    return HttpResponse("Transaction Module")

def report_dashboard(request):
    return HttpResponse("Report Module")

def view_account(request, id):
    account = Account.objects.get(acc_rid=id)
    return render(request, 'accounts/view_account.html', {'account': account})
def edit_account(request, id):
    account = Account.objects.get(acc_rid=id)

    if request.method == 'POST':
        account.acc_name = request.POST['acc_name']
        account.acc_place = request.POST['acc_place']
        account.acc_phone = request.POST['acc_phone']
        account.acc_address = request.POST['acc_address']

        account.acc_is_customer = request.POST.get('acc_is_customer') == "True"
        account.acc_is_supplier = request.POST.get('acc_is_supplier') == "True"
        account.acc_is_staff = request.POST.get('acc_is_staff') == "True"

        account.save()
        return redirect('account_list')

    return render(request, 'accounts/edit_account.html', {'account': account})

def delete_account(request, id):
    account = Account.objects.get(acc_rid=id)
    account.delete()
    return redirect('account_list')

def get_next_sequence(entity):
    seq = SequenceGenerator.objects.get(seq_entity=entity)

    seq.seq_number += 1
    seq.save()

    number = str(seq.seq_number).zfill(seq.num_digits)

    return f"{seq.seq_prefix}{number}{seq.seq_suffix or ''}"
def get_preview_sequence(entity):
    seq = SequenceGenerator.objects.get(seq_entity=entity)
    number = str(seq.seq_number + 1).zfill(seq.num_digits)
    return f"{seq.seq_prefix}{number}{seq.seq_suffix or ''}"