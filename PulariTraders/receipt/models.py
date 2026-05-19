from datetime import date

from django.db import models
from django.utils import timezone


class Receipt(models.Model):
    rcpt_rid = models.AutoField(primary_key=True)
    rcpt_status = models.CharField(max_length=12)
    rcpt_no = models.CharField(max_length=12, unique=True)
    rcpt_date = models.DateField()
    rcpt_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rcpt_acc_rid = models.IntegerField()
    rcpt_notes = models.CharField(max_length=520, blank=True, null=True)
    rcpt_created_date = models.DateField()
    rcpt_modified_date = models.DateField()

    class Meta:
        db_table = 'receipt'
        ordering = ['-rcpt_rid']

    def __str__(self):
        return self.rcpt_no

    @property
    def bh_display_name(self):
        return f"{self.rcpt_no} - ₹{self.rcpt_amt}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.rcpt_rid = None
        obj.rcpt_status = 'Active'
        obj.rcpt_no = ""
        obj.rcpt_date = date.today()
        obj.rcpt_amt = 0
        obj.rcpt_acc_rid = None
        obj.rcpt_notes = ""
        return obj