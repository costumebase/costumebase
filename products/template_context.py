from itertools import product
from .models import Category, Product, Variants
from cart.models import ShopCart

from dashboard.models import Vendor_Payment
from order.models import Order, OrderProduct
from django.db.models import Count
from django.db.models.aggregates import Max, Min, Count

def get_filters(request):


    category=Product.objects.distinct().values('category__name', 'category__children__name', 'category__parent__name','category__id').annotate(category_count=Count('category'))
    shop= Product.objects.distinct().values('shop__name', 'shop__id').annotate(shop_count=Count('shop'))
    
    color = Variants.objects.distinct().values('color__name', 'color__id', 'color__code').annotate(color_count=Count('color'))
    size = Variants.objects.distinct().values('size__code', 'size__id').annotate(size_count=Count('size'))
    minMaxPrice=Variants.objects.aggregate(Min('price'),Max('price'))

    current_user = request.user
     # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    order_count = Order.objects.filter(user_id=current_user.id, ordered=True)
    order_canceld = Order.objects.filter(user_id=current_user.id, ordered=True, status='Canceled').count()


    data = {
        'cats':category,
        'shop':shop,
        'color':color,
        'size':size,
        'minMaxPrice':minMaxPrice,
        'shopcart':shopcart,
        'order_count':order_count,
        'order_canceld':order_canceld,
    }
    return data