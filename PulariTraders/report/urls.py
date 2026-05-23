from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.report, name="report"),
    path("generate_report/", views.generate_report, name="generate_report"),
    path("print_preview/", TemplateView.as_view(template_name="report/stock_transaction_report.html"), name="print_preview"),
]