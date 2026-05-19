from django.db import models
from datetime import date, datetime
from django.utils import timezone


class SaleReturnHeader(models.Model):
    sr_rid = models.AutoField(primary_key=True)
    sr_status = models.CharField(max_length=12, default='Active')
    sr_sale_return_no = models.CharField(max_length=50, unique=True)
    sr_sale_return_date = models.DateField()
    sr_notes = models.CharField(max_length=520, blank=True, null=True)
    sr_counter_sale = models.BooleanField(default=False)
    sr_acc_rid = models.IntegerField()
    sr_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sr_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sr_net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sr_created_date = models.DateTimeField(auto_now_add=True)
    sr_modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sale_return_header'
        ordering = ['-sr_rid']

    def __str__(self):
        return self.sr_sale_return_no

    @property
    def sr_display_name(self):
        return f"{self.sr_sale_return_no} - ₹{self.sr_amount}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.sr_status = 'Active'
        obj.sr_rid = None
        obj.sr_sale_return_no = ""
        obj.sr_sale_return_date = date.today()
        obj.sr_acc_rid = None
        obj.sr_notes = ""
        obj.sr_counter_sale = False
        obj.sr_amount = 0
        obj.sr_discount = 0
        obj.sr_net_amount = 0
        return obj


class SaleReturnDetail(models.Model):
    srd_rid = models.AutoField(primary_key=True)
    srd_sr_rid = models.IntegerField()
    srd_item_rid = models.IntegerField()
    srd_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    srd_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    srd_total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'sale_return_detail'
        ordering = ['srd_rid']

    def __str__(self):
        return f"{self.srd_item_rid} - {self.srd_qty}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.srd_rid = None
        obj.srd_sr_rid = None
        obj.srd_item_rid = None
        obj.srd_qty = 0
        obj.srd_amount = 0
        obj.srd_total_amount = 0
        return obj