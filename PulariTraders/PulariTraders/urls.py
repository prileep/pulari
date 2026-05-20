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

from account import views
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),
    path('', views.home, name='home'),

    path('bill/', include('bill.urls')),
    path('Bill/', include('bill.urls')),   # optional alias

    path('items/', include('items.urls')),

    path('billreturn/', include('salereturn.urls')),
    path('BillReturn/', include('salereturn.urls')),   # optional alias

    path('purchasereturn/', include('purchasereturn.urls')),
    path('PurchaseReturn/', include('purchasereturn.urls')),   # optional alias

    path('purchase/', include('purchase.urls')),
    path('Purchase/', include('purchase.urls')),   # optional alias

    path('transactionbrowser/',include('transactionbrowser.urls')),

    path('receipt/',include('receipt.urls')),
    path('Receipt/',include('receipt.urls')),   # optional alias

    path('discount/',include('discount.urls')),
    path('Discount/',include('discount.urls')),   # optional alias

    path('payment/',include('payment.urls')),
    path('Payment/',include('payment.urls')),   # optional alias
        
]
