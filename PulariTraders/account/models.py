from django.db import models



class Account(models.Model):
    acc_rid = models.AutoField(primary_key=True)   
    acc_code = models.CharField(max_length=10, unique=True)  

    acc_name = models.CharField(max_length=60)
    acc_place = models.CharField(max_length=60)
    acc_phone = models.CharField(max_length=30)
    acc_address =models.CharField(max_length=120)
    acc_is_customer = models.CharField(max_length=3, default='No')
    acc_is_supplier = models.CharField(max_length=3, default='No')
    acc_is_staff = models.CharField(max_length=3, default='No')
    acc_disp_name = models.CharField(
        max_length=130,
        blank=True,
        null=True
    )
    def __str__(self):
        return self.acc_name
    class Meta:
        db_table = 'account'
        constraints = [
            models.UniqueConstraint(
                fields=['acc_name', 'acc_place'],
                name='unique_name_place'
            )
        ]
    def save(self, *args, **kwargs):

        if self.acc_name:
            self.acc_name = self.acc_name.upper()

        if self.acc_place:
            self.acc_place = self.acc_place.upper()

        if self.acc_address:
            self.acc_address = self.acc_address.upper()

        if self.acc_place:
            self.acc_disp_name = f"{self.acc_name} - {self.acc_place}"
        else:
            self.acc_disp_name = self.acc_name

        super().save(*args, **kwargs)

class SequenceGenerator(models.Model):
    seq_prefix = models.CharField(max_length=10)
    seq_suffix = models.CharField(max_length=10, blank=True, null=True)
    seq_number = models.IntegerField(default=0)
    seq_entity = models.CharField(max_length=50)
    num_digits = models.IntegerField()

    class Meta:
        db_table = 'sequence_generator'  

