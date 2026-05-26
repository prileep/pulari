from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.report, name="report"),
    path("printreport/", views.printreport, name="printreport"),

]