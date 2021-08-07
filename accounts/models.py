from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.forms.widgets import NumberInput
from django.utils.translation import ugettext_lazy as _
from accounts.managers import CustomUserManager
from django.core.validators import RegexValidator
from django.dispatch import receiver
import random



class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    # phone_regex = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True, error_messages={'unique':"This phone has already been registered."})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_buyer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    objects = CustomUserManager() 

    def __str__(self):
        return self.email
    
    
    class Meta:
        verbose_name_plural='1. Users'





class Code(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.number
        
    class Meta:
        verbose_name_plural='0. Vendor Auth Code'


    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []
        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save(*args, **kwargs)


def code_save(sender, instance, created, *args, **kwargs):

    if created:
        buyer = Code.objects.create(user=instance)

post_save.connect(code_save, sender=User)




class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
 

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name_plural='2. Vendors'



class Business_Profile(models.Model):
    user = models.ForeignKey(Vendor, related_name='vendor_profile', on_delete=models.CASCADE)
    business_name = models.CharField(max_length=50)
    address1 = models.CharField(verbose_name="Address 1", max_length=250)
    address2 = models.CharField(verbose_name="Address 2", max_length=250)
    city = models.CharField(verbose_name="City", max_length=50)
    state = models.CharField(verbose_name="State", max_length=20)
    pincode = models.CharField(verbose_name="PIN Code", max_length=6)
    gst_details = models.FileField(upload_to='gst_file')
    business_proof = models.FileField(upload_to='business_proof')
    pan_card = models.FileField(upload_to='pan_card')
    aadhar_card = models.FileField(upload_to='aadhar_card')

    class Meta:
        verbose_name_plural='3. Vendor_Details'





class Buyer(models.Model):
    user = models.OneToOneField(User, related_name='buyer', on_delete=models.CASCADE)
    your_name = models.CharField(max_length=50)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name_plural='4. Buyers'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(blank=True, max_length=20)
    last_name = models.CharField(blank=True, max_length=20)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    address_optional = models.CharField(blank=True, max_length=150)
    country = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=20)
    province = models.CharField(blank=True, max_length=100)
    zip = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return str(self.user)


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)










class UserOTP(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	time_st = models.DateTimeField(auto_now = True)
	otp = models.SmallIntegerField()