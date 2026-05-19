from datetime import date

from django.db import models
from django.utils import timezone


class PurchaseHeader(models.Model):
    ph_rid = models.AutoField(primary_key=True)
    ph_status = models.CharField(max_length=12, default='Active')
    ph_purchase_no = models.CharField(max_length=50, unique=True)
    ph_purchase_date = models.DateField()
    ph_notes = models.CharField(max_length=520, blank=True, null=True)
    ph_counter_sale = models.BooleanField(default=False)
    ph_acc_rid = models.IntegerField()
    ph_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ph_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ph_net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ph_created_date = models.DateTimeField(auto_now_add=True)
    ph_modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchase_header'
        ordering = ['-ph_rid']

    def __str__(self):
        return self.ph_purchase_no

    @property
    def ph_display_name(self):
        return f"{self.ph_purchase_no} - ₹{self.ph_amount}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.ph_status = 'Active'
        obj.ph_rid = None
        obj.ph_purchase_no = ""
        obj.ph_purchase_date = date.today()
        obj.ph_acc_rid = None
        obj.ph_notes = ""
        obj.ph_counter_sale = False
        obj.ph_amount = 0
        obj.ph_discount = 0
        obj.ph_net_amount = 0
        return obj


class PurchaseDetail(models.Model):
    pd_rid = models.AutoField(primary_key=True)
    pd_ph_rid = models.IntegerField()
    pd_item_rid = models.IntegerField()
    pd_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pd_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pd_total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'purchase_detail'
        ordering = ['pd_rid']

    def __str__(self):
        return f"{self.pd_item_rid} - {self.pd_qty}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.pd_rid = None
        obj.pd_ph_rid = None
        obj.pd_item_rid = None
        obj.pd_qty = 0
        obj.pd_amount = 0
        obj.pd_total_amount = 0
        return obj