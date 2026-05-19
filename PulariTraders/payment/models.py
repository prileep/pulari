from datetime import date

from django.db import models
from django.utils import timezone


class Payment(models.Model):
    pay_rid = models.AutoField(primary_key=True)
    pay_status = models.CharField(max_length=12)
    pay_no = models.CharField(max_length=12, unique=True)
    pay_date = models.DateField()
    pay_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pay_acc_rid = models.IntegerField()
    pay_notes = models.CharField(max_length=520, blank=True, null=True)
    pay_created_date = models.DateField()
    pay_modified_date = models.DateField()

    class Meta:
        db_table = 'payment'
        ordering = ['-pay_rid']

    def __str__(self):
        return self.pay_no

    @property
    def bh_display_name(self):
        return f"{self.pay_no} - ₹{self.pay_amt}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.pay_rid = None
        obj.pay_status = 'Active'
        obj.pay_no = ""
        obj.pay_date = date.today()
        obj.pay_amt = 0
        obj.pay_acc_rid = None
        obj.pay_notes = ""
        return obj