from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import mark_safe
from django.shortcuts import reverse
from django.forms import ModelForm
import uuid

from .utilis import create_new_ref_number

from accounts.models import Vendor, Buyer





class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_index=True)
    image = models.ImageField(upload_to="category/images", null=True, blank=True)
    top_category = models.BooleanField(default=False)
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural='2. Categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product:category-detail", kwargs={
            'slug': self.slug
        })

    class MPTTMeta:
        order_insertion_by = ['name']


class Shop(models.Model):
    name=models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, related_name='shop_owner', on_delete=models.CASCADE,
                                null=True, blank=True)  # need to be changed
    image=models.ImageField(upload_to="shop/images")
    discription = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural='3. Shops'

    def __str__(self):
        return self.name
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

class Brand(models.Model):
    name=models.CharField(max_length=100, unique=True)
    image=models.ImageField(upload_to="brand/images")

    class Meta:
        verbose_name_plural='4. Brands'

    def __str__(self):
        return self.name


class Product(models.Model):
    
    VARIANTS = (
            ('None', 'None'),
            ('Size', 'Size'),
            ('Color', 'Color'),
            ('Size-Color', 'Size-Color'),

        )

    vendor = models.ForeignKey(Vendor, related_name='vendors', on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey(Shop, related_name='shops', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brands', on_delete=models.CASCADE, null=True, blank=True)
    category = TreeForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
     
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)

    image_main = models.ImageField(upload_to='product/images')
    variant=models.CharField(max_length=10,choices=VARIANTS, default='Color')
    amount=models.IntegerField(default=0)

    description = models.TextField(verbose_name='Product short description', max_length=500, blank=False)

    is_for_sale = models.BooleanField(default=True)
    is_free_shipping = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural='1. Products'

        

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image_main.url))

    def get_absolute_url(self):
        return reverse("product:product-detail", kwargs={
            'slug': self.slug
        })
    


class Images(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='vendor_image', on_delete=models.CASCADE, null=True, blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='product/images')

    def __str__(self):
        return self.name
    
    def image_tag(self):

        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        else:

           return "/static/images/gf.png"

    class Meta:
        verbose_name_plural='5. Images'


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, unique=True)  

    def __str__(self):
        return self.name

    def color_tag(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.code))

    class Meta:
        verbose_name_plural='6. Colors'


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, unique=True)  

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name_plural='7. Sizes'


class Variants(models.Model):
    
    vendor = models.ForeignKey(Vendor, related_name='vendor_variation', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)    
    quantity = models.IntegerField(default=1)
    price = models.FloatField()

    def __str__(self):
        return self.product.name

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

    class Meta:
        verbose_name_plural='8. Variants'



class Comment(models.Model):

    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural='9. Comments'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']



