from datetime import date
from django.utils import timezone  # Standard utility for Django tracking

from django.db import models
from django.utils import timezone


class BillHeader(models.Model):
    bh_rid = models.AutoField(primary_key=True)
    bh_status = models.CharField(max_length=12, default='Active')
    bh_bill_no = models.CharField(max_length=50, unique=True)
    bh_bill_date = models.DateField()
    bh_notes = models.CharField(max_length=520, blank=True, null=True)
    bh_counter_sale = models.BooleanField(default=False)
    bh_acc_rid = models.IntegerField()
    bh_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bh_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bh_net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bh_rcpt_rid = models.IntegerField()
    bh_rcpt_no = models.CharField(max_length=12)
    bh_created_date = models.DateTimeField()
    bh_modified_date = models.DateTimeField()

    class Meta:
        db_table = 'bill_header'
        ordering = ['-bh_rid']

    def __str__(self):
        return self.bh_bill_no

    @property
    def bh_display_name(self):
        return f"{self.bh_bill_no} - ₹{self.bh_amount}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.bh_status = 'Active'
        obj.bh_rid = None
        obj.bh_bill_no = ""
        obj.bh_bill_date = date.today()
        obj.bh_acc_rid = None
        obj.bh_notes = ""
        obj.bh_counter_sale = False
        obj.bh_amount = 0
        obj.bh_discount = 0
        obj.bh_net_amount = 0
        return obj


class BillDetail(models.Model):
    bd_rid = models.AutoField(primary_key=True)
    bd_bh_rid = models.IntegerField()
    bd_item_rid = models.IntegerField()
    bd_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bd_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bd_total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'bill_detail'
        ordering = ['bd_rid']

    def __str__(self):
        return f"{self.bd_item_rid} - {self.bd_qty}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.bd_rid = None
        obj.bd_bh_rid = None
        obj.bd_item_rid = None
        obj.bd_qty = 0
        obj.bd_amount = 0
        obj.bd_total_amount = 0
        return obj