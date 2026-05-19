from django.db import models
import re

class Item(models.Model):
    item_rid = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=60, unique=True)
    item_code = models.CharField(max_length=10, unique=True)
    item_gst = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    item_mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_display_name = models.CharField(max_length=70, blank=True, null=True)
    item_stk = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'item'

    def __str__(self):
        return self.item_name

    @property
    def display_name(self):
        return self.item_display_name or f"{self.item_name} - {self.item_code}"
    def save(self, *args, **kwargs):
        self.item_display_name = f"{self.item_name} - {self.item_code}"
        super().save(*args, **kwargs)

    @classmethod
    def empty(cls):
        obj = cls()
        obj.item_rid = 0
        obj.item_name = ""
        obj.item_code = ""
        obj.item_gst = 0
        obj.item_mrp = 0
        obj.item_sale_price = 0
        obj.item_display_name = ""
        obj.item_stk = 0
        return obj