"""
URL configuration for PulariTraders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.account_list, name='account_list'),   # ✅ correct
  
    # ACCOUNT
    path('account/', views.account_list, name='account_list'),
  # PURCHASE
    path('purchase/', views.purchase_list, name='purchase_list'),
    path('search-customer/', views.search_customer, name='search_customer'),
    # RECEIPT
    path('receipt/', views.receipt_list, name='receipt_list'),

    # TRANSACTION
    path('transaction/', views.transaction_list, name='transaction_list'),

    # REPORT
    path('report/', views.report_dashboard, name='report_dashboard'),

    # accounts/urls.py
path('account/<int:pk>/', views.account, name='account'),
path('account/delete/<int:id>/', views.delete_account, name='delete_account'),

] 
