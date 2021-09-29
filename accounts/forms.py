from django import forms
from .models import User, Vendor, Buyer, Code
from django.db import transaction

from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Code', help_text="Enter Verification Code")

    class Meta:
        model = Code
        fields = ('number',)


class CustomerSignUpForm(UserCreationForm):
    your_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('your_name', 'email', 'password1', 'password2', )
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_buyer = True
        user.save()
        customer = Buyer.objects.create(user=user)
        customer.your_name=self.cleaned_data.get('your_name')
        customer.save()
        
        return user



class VendorSignUpForm(UserCreationForm):   
    # phone_regex = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    # phone = forms.RegexField(regex = r'^\+?1?\d{9,10}$', max_length=10)
    # business_name = forms.CharField(required=True)
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'password1', 'password2', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        customer = Vendor.objects.create(user=user)
        # customer.business_name=self.cleaned_data.get('business_name')
        # customer.save()
        return user






