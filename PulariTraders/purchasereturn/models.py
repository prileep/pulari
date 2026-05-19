from datetime import date

from django.db import models
from django.utils import timezone


class PurchasereturnHeader(models.Model):
    pr_rid = models.AutoField(primary_key=True)
    pr_status = models.CharField(max_length=12, default='Active')
    pr_purchase_return_no = models.CharField(max_length=50, unique=True)
    pr_purchase_return_date = models.DateField()
    pr_notes = models.CharField(max_length=520, blank=True, null=True)
    pr_counter_purchase = models.BooleanField(default=False)
    pr_acc_rid = models.IntegerField()
    pr_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pr_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pr_net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pr_created_date = models.DateTimeField(auto_now_add=True)
    pr_modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchase_return_header'
        ordering = ['-pr_rid']

    def __str__(self):
        return self.pr_purchase_return_no

    @property
    def pr_display_name(self):
        return f"{self.pr_purchase_return_no} - ₹{self.pr_amount}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.pr_status = 'Active'
        obj.pr_rid = None
        obj.pr_purchase_return_no = ""
        obj.pr_purchase_return_date = date.today()
        obj.pr_acc_rid = None
        obj.pr_notes = ""
        obj.pr_counter_sale = False
        obj.pr_amount = 0
        obj.pr_discount = 0
        obj.pr_net_amount = 0
        return obj


class PurchasereturnDetail(models.Model):
    prd_rid = models.AutoField(primary_key=True)
    prd_pr_rid = models.IntegerField()
    prd_item_rid = models.IntegerField()
    prd_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prd_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prd_total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'purchase_return_detail'
        ordering = ['prd_rid']

    def __str__(self):
        return f"{self.prd_item_rid} - {self.prd_qty}"
    

    @classmethod
    def empty(cls):
        obj = cls()
        obj.prd_rid = None
        obj.prd_bh_rid = None
        obj.prd_item_rid = None
        obj.prd_qty = 0
        obj.prd_amount = 0
        obj.prd_total_amount = 0
        return obj