from django.db import models
from datetime import date, datetime
from django.utils import timezone


class BillReturnHeader(models.Model):
    br_rid = models.AutoField(primary_key=True)
    br_status = models.CharField(max_length=12, default='Active')
    br_bill_return_no = models.CharField(max_length=50, unique=True)
    br_bill_return_date = models.DateField()
    br_notes = models.CharField(max_length=520, blank=True, null=True)
    br_counter_sale = models.BooleanField(default=False)
    br_acc_rid = models.IntegerField()
    br_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    br_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    br_net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    br_created_date = models.DateTimeField()
    br_modified_date = models.DateTimeField()

    class Meta:
        db_table = 'bill_return_header'
        ordering = ['-br_rid']

    def __str__(self):
        return self.br_bill_return_no

    @property
    def br_display_name(self):
        return f"{self.br_bill_return_no} - ₹{self.br_amount}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.br_status = 'Active'
        obj.br_rid = None
        obj.br_bill_return_no = ""
        obj.br_bill_return_date = date.today()
        obj.br_acc_rid = None
        obj.br_notes = ""
        obj.br_counter_sale = False
        obj.br_amount = 0
        obj.br_discount = 0
        obj.br_net_amount = 0
        return obj


class BillReturnDetail(models.Model):
    brd_rid = models.AutoField(primary_key=True)
    brd_br_rid = models.IntegerField()
    brd_item_rid = models.IntegerField()
    brd_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    brd_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    brd_total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'bill_return_detail'
        ordering = ['brd_rid']

    def __str__(self):
        return f"{self.brd_item_rid} - {self.brd_qty}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.brd_rid = None
        obj.brd_br_rid = None
        obj.brd_item_rid = None
        obj.brd_qty = 0
        obj.brd_amount = 0
        obj.brd_total_amount = 0
        return obj