from django import forms
from django.forms import fields
from products.models import *


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['vendor']
        fields = ['brand', 'shop', 'category', 'variant', 'amount', 'name', 'price', 
        'discount_price', 'image_main', 'is_for_sale', 'is_free_shipping', 'description']


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Images
        exclude = ['vendor']
        fields = ['product', 'name', 'image']

   

class ProductVariation(forms.ModelForm):
    class Meta:
        model = Variants
        exclude = ['vendor']
        fields = ['name', 'product', 'color', 'size', 'image_id', 'quantity', 'price']

        