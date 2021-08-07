from django.db import models
from accounts.models import Vendor
# Create your models here.


class Vendor_Payment(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='vendor_payment', on_delete=models.CASCADE, null=True, blank=True)
    vendor_paid_total = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor.user.email

    
