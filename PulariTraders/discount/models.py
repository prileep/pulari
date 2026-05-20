from datetime import date

from django.db import models
from django.utils import timezone


class Discount(models.Model):
    disc_rid = models.AutoField(primary_key=True)
    disc_status = models.CharField(max_length=12)
    disc_no = models.CharField(max_length=12, unique=True)
    disc_date = models.DateField()
    disc_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    disc_acc_rid = models.IntegerField()
    disc_notes = models.CharField(max_length=520, blank=True, null=True)
    disc_created_date = models.DateField()
    disc_modified_date = models.DateField()

    class Meta:
        db_table = 'discount'
        ordering = ['-disc_rid']

    def __str__(self):
        return self.disc_no

    @property
    def bh_display_name(self):
        return f"{self.disc_no} - ₹{self.disc_amt}"

    @classmethod
    def empty(cls):
        obj = cls()
        obj.disc_rid = None
        obj.disc_status = 'Active'
        obj.disc_no = ""
        obj.disc_date = date.today()
        obj.disc_amt = 0
        obj.disc_acc_rid = None
        obj.disc_notes = ""
        return obj