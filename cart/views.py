from django.shortcuts import redirect, render
from django.views import generic
from products.models import *
from .models import *
from order.models import *

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from .forms import CouponForm



@login_required(login_url='/register/customer_login/')
def addtoshopcart(request,id):
   
    current_user = request.user  # Access User Session information
    product= Product.objects.get(pk=id)
    print(product, "hollly fujck")

    variantid = request.POST.get('variantid', None)

    print(variantid, 'checking variaents id man')

    if product.variant != 'None':
         # from variant add to cart

         # it will show if it has in cart
    
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)
        
        print(checkinvariant, "variantid vs variant_id")

        if checkinvariant:
            control = 1 # The product is in the cart
            print("i am variation but still not in cart ")

        else:
            control = 0 # The product is not in the cart"""
            print("i am variation but in cart ")

        print("i do have variations")
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart

        print(checkinproduct, "product_id vs id")

        if checkinproduct:
            control = 1 # The product is in the cart
            print('i in cart as product')
        else:
            control = 0 # The product is not in the cart"""
            print('im not in cart as product')
        print("i dont have any variations")
        

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                    print(data, "checking none variatents formvalidate ")
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                    print(data, "checking variatents formvalidate ")
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
                print("saved data let's go")
        messages.success(request, "Product added to Shopcart ")
        return redirect('cart:shopcart')

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id = None
            data.save()  #

        messages.success(request, "Product added to Shopcart")
        return redirect('cart:shopcart')

# class OrderSummaryView(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.filter(user=self.request.user, ordered=False)
#             context = {
#                 'order': order,
#                 'couponform': CouponForm(),
#                 'DISPLAY_COUPON_FORM': True
#             }
#             return render(self.request, 'eco/basket.html', context)
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("eco:EcoIndex")

# def get_total(self):
#     total = 0
#     amount = models.FloatField()
#     for order_item in self.items.all():
#         total += order_item.get_final_price()
#     if self.coupon:
#         total -= self.coupon.amount
#     return total



def shopcart(request):
    current_user = request.user
    category = Category.objects.all()  # Access User Session information
    shopcart = ShopCart.objects.filter(user=request.user)

    total = 0
    for i in shopcart:

        if i.product.variant == "None":

            total += i.product.price * i.quantity
        else:
            if i.variant != None:
                total += i.variant.price * i.quantity
  



    #     print(total, "that's mean i am not ")

        
    context={'shopcart': shopcart,
             'category': category,
             'total':total,

             }
    return render(request,'cart.html',context)





@login_required(login_url='/register/customer_login/')

def deletefromcart(request,id):
    current_user = request.user
    ShopCart.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, "Your item deleted form Cart.")
    return redirect('cart:shopcart')


@login_required(login_url='/register/customer_login/')

def remove_one_product(request, id):
    current_user = request.user
    product = Product.objects.get(pk=id)
    print(product, 'say your product ')                                  
    shopcart = ShopCart.objects.filter(product_id=id, user_id=current_user.id)
    print(shopcart, "say your")
    if shopcart.exists():
        for shop in shopcart:
            if shop.quantity > 1:
                shop.quantity -= 1
                shop.save()
                print("i am ot less than 1")
            else:
                shop.delete()
                print("i am more than 1 ")
    else:
        print("Your cart has minumum product")

    return redirect('cart:shopcart')

@login_required(login_url='/register/customer_login/')

def add_one_product(request, id):
    current_user = request.user
    product = Product.objects.get(pk=id)
    print(product, 'say your product ')                                  
    shopcart = ShopCart.objects.filter(product_id=id, user_id=current_user.id)
    print(shopcart, "say your")
    if shopcart.exists():
        for shop in shopcart:
            if shop.quantity > 0:
                shop.quantity += 1
                shop.save()
                print("i am ot less than 1")
            else:
                shop.add(product)
                print("i am more than 1 ")
    else:
        print("Your cart has minumum product")

    return redirect('cart:shopcart')



@login_required(login_url='/register/customer_login/')

def remove_variant_product(request, id):
    current_user = request.user
    product = Variants.objects.get(pk=id)
    print(product, 'say your product ')

    shopcart = ShopCart.objects.filter(variant_id=product.id, user_id=current_user.id)
    print(shopcart.values(), 'trying to price some values')

    if shopcart.exists():
        for shop in shopcart:
            if shop.quantity > 1:
                shop.quantity -= 1
                shop.save()
                print("i am ot less than 1")
            else:
                shop.delete()
                print("i am more than 1 ")
    else:
        print("Your cart has minumum product")

    return redirect('cart:shopcart')

def add_variant_product(request, id):

    current_user = request.user
    product = Variants.objects.get(pk=id)
    print(product, 'say your product ')

    shopcart = ShopCart.objects.filter(variant_id=product.id, user_id=current_user.id)
    print(shopcart.values(), 'trying to price some values')

    if shopcart.exists():
        for shop in shopcart:
            if shop.quantity > 0:
                shop.quantity += 1
                shop.save()
                print("i am ot less than 1")
            else:
                shop.delete()
                print("i am more than 1 ")
    else:
        print("Your cart has minumum product")

    return redirect('cart:shopcart')



          

