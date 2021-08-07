from django import template
from django.db.models import Sum
from django.urls import reverse


from cart.models import ShopCart

register = template.Library()




@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count



@register.simple_tag
def shopcarttotal(userid):

    shopcart = ShopCart.objects.filter(user_id=userid)
    total = 0
    for i in shopcart:

        if i.product.variant == "None":

            total += i.product.price * i.quantity
        else:
            if i.variant != None:
                total += i.variant.price * i.quantity
    return total
