from django.urls import path
from . import views

urlpatterns = [
    path("", views.transaction_browser, name="transactionbrowser"),
    path("transaction-search/", views.transaction_search, name="transaction_search"),
]