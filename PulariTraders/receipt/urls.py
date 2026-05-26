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
from . import views
urlpatterns = [

    path('', views.receipt, name='receipt'),
    path('<int:rid>/', views.receipt, name='rid'),
    
    # AJAX / API Endpoints
    path('api/customer-balance-sheet/', views.get_customer_balance_sheet, name='get_customer_balance_sheet'),
]
