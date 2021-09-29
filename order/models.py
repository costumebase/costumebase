from django.db import models

from django_countries.fields import CountryField

from cart.models import *



STATUS = (


        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),

    )


METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("RazorPay", "RazorPay"),
    ("Stripe", "Stripe"),
)

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # vendor = models.ForeignKey(Vendor, related_name='vendors_order', on_delete=models.CASCADE, null=True, blank=True)

    code = models.CharField(max_length=5, editable=False )
    ref_code = models.CharField(max_length=50, blank=True)
    total = models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.TextField(blank=True)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    ordered = models.BooleanField(default=False)

    first_name = models.CharField(max_length=10, blank=True)
    last_name = models.CharField(max_length=10, blank=True)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    address_optional = models.CharField(blank=True, max_length=150)
    country = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=20)
    province = models.CharField(blank=True, max_length=100)
    zip = models.CharField(blank=True, max_length=100)

    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    order_status = models.CharField(max_length=50, blank=True, choices=STATUS) # gotta change this one

    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','address',
        'address_optional', 'country', 'city', 'province', 'zip', 'adminnote']

# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name','last_name',
#         'address','phone','city','country']

class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='vendor_orderproduct', on_delete=models.CASCADE, null=True, blank=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    variant_amount = models.FloatField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS, default='New')
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.name


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = '2. Addresses'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    orders = models.ForeignKey(Order, related_name='vendor_payment', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField()
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = '3. Coupons'


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name_plural = '4. Refund'


    