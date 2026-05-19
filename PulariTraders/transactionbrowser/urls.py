from django.urls import path
from . import views

urlpatterns = [
    path("", views.transaction_browser, name="transactionbrowser"),
    path("transaction-search/", views.transaction_search, name="transaction_search"),
    path("print/", views.transaction_print, name="transaction_print"),
    path("printbyaccount/", views.transaction_print_by_account, name="transaction_print"),
]