
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Address




PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    city = forms.CharField(required=False)
    province = forms.CharField(required=False)
    shipping_zip = forms.CharField(required=False)


    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class Account(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user',)
        fields = (
            'street_address', 'apartment_address', 'country','zip',
            'address_type', 'default',
        )
