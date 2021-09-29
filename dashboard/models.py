from django.db import models
from accounts.models import *

# Create your models here.


class Vendor_Payment(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='vendor_payment', on_delete=models.CASCADE, null=True, blank=True)
    vendor_paid_total = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor.user.email




class Messages(models.Model):
    description = models.TextField()
    sender_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"

    class Meta:
        ordering = ('timestamp',)


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.IntegerField()

    def __str__(self):
        return f"{self.friend}"

