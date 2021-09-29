from cart.views import shopcart
from typing import Generic
import string
from django.http import response
import razorpay
from django.views.decorators.csrf import csrf_exempt

from django.http import request, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from products.models import *
from .forms import *

razorpaykey=settings.RAZORKEY 
razorpaysecret=settings.RAZORSECRET


class checkoutt(generic.TemplateView):
    template_name = 'checkoutt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['category'] = Category.objects.all()
        return context


@login_required(login_url='/register/customer_login/')

@csrf_exempt
def payment_success(request):
    current_user = request.user
    category = Category.objects.all()
    # order = Order.objects.filter(user_id=current_user.id, ordered=False)
    orders = Order.objects.filter(user_id=current_user.id, ordered=True)
    if request.method == "POST":
        response = request.POST
        params_dict = {

            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_signature': response['razorpay_signature']

                  }

        print(params_dict, 'those params')
        client = razorpay.Client(auth=(razorpaykey, razorpaysecret))
        client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(user=request.user, paid=False, order_id=response['razorpay_order_id'])

        payment.payment_id = response['razorpay_payment_id']
        payment.paid = True
        payment.save()
        if payment.paid == True:
            print("cold dude")
            lol = Order.objects.filter(user=request.user, ordered=False).last()
            # lol.total = total
            # lol.user = request.user
            lol.ordered = True
            lol.ref_code = create_ref_code()
            lol.save()

            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                if rs.product.variant=='None':
                    product = Product.objects.get(id=rs.product_id)
                    print("hey you printing ", product)
                    product.amount -= rs.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.variant_id)
                    variant.quantity -= rs.quantity
                    variant.save()
                    print("i am not none product so reduce me", variant)
            
                #************ <> *****************

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has completed, Thank you :)")
            return redirect('order:user-order')
        else:
            return redirect('order:razor')

    return redirect('order:user-order')



@login_required(login_url='/register/customer_login/')

def razor(request):

    current_user = request.user
    category = Category.objects.all()
    order = Order.objects.filter(user_id=current_user.id, ordered=False).last()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    tot = order.total
    print("hey get some total", tot)

    if order:
        total = int(order.total * 100)
        print(total, 'fuck you')

        if order.address and order.city:
            print("you have billling adress")

            client = razorpay.Client(auth=(razorpaykey, razorpaysecret))
            payment = client.order.create({'amount':total,'currency':'INR','payment_capture':1})
            status = payment['status']

            print("printitng id ", payment['id'])

          

            if status == "created":
                bar = Payment(
                user=request.user,
                orders = order,
                amount=total,
                order_id = payment['id'],
                )
                bar.save()
                      

            else:
                messages.info(request, "Sorry we couldn't placed your order")
                return redirect("order:payment")

        else:
            messages.info(request, "You do not have an billing addresses")
            return redirect("order:checkout")
        
        context = { 
            'category':category,
            'payment':payment,
            'shopcart':shopcart,
            'total':tot,
        }
        return render(request, 'pay.html', context)

    else:
        print("you dont have fuck due")
        messages.info(request, "You do not have an active order")
        return redirect("order:checkout")
       


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid
from django.utils.decorators import method_decorator
from products.decorators import customer_required

@method_decorator([login_required, customer_required], name='dispatch')

class Checkout(LoginRequiredMixin, generic.View):
    login_url = '/register/customer_login/'

    def get(self, *args, **kwargs):
        try:
            current_user = self.request.user
            category = Category.objects.all()            
            profile = UserProfile.objects.get(user_id=current_user.id)
            ordered = Order.objects.filter(user_id=current_user.id, ordered=False).last()
            order = ShopCart.objects.filter(user_id=current_user.id)
            print(order.values(), "checkout get function")
            total = 0
            for i in order:

                if i.product.variant == "None":

                    total += i.product.price * i.quantity
                else:
                    if i.variant != None:
                        total += i.variant.price * i.quantity

            form = OrderForm()

            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'ordered':ordered,
                'total':total,
                'profile':profile,
                'category':category,
                'DISPLAY_COUPON_FORM': True
            }
       
            return render(self.request, "checkout.html", context)
                
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("order:checkout")

    def post(self, *args, **kwargs):
        form = OrderForm(self.request.POST or None)
        current_user = self.request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        
        total = 0
        for i in shopcart:

            if i.product.variant == "None":

                total += i.product.price * i.quantity
            else:
                if i.variant != None:
                    total += i.variant.price * i.quantity

        print(total, "hey whats up buddy ")

        if shopcart.exists():
            order = Order()

        
        if form.is_valid():
            order = Order()

            order.user_id = current_user.id
            order.total = total
            order.first_name = form.cleaned_data['first_name'] 
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']
            order.address_optional = form.cleaned_data['address_optional']
            order.country = form.cleaned_data['country']
            order.city = form.cleaned_data['city']
            order.province = form.cleaned_data['province']
            order.zip = form.cleaned_data['zip']
            order.adminnote = form.cleaned_data['adminnote']
            order.ip = self.request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            order.code =  ordercode
            order.save()

            profile = UserProfile.objects.get(user_id=current_user.id)
            profile.first_name = order.first_name
            profile.last_name = order.last_name 
            profile.phone = order.phone
            profile.address = order.address 
            profile.address_optional = order.address_optional
            profile.country = order.country
            profile.city = order.city
            profile.province = order.province
            profile.zip = order.zip
            profile.save()



            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = order.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.vendor       = rs.product.vendor
                detail.quantity     = rs.quantity

                if rs.product.variant == 'None':
                    detail.price    = rs.product.price
                else:
                    detail.price = rs.variant.price
                    detail.variant_amount = rs.varamount

                detail.variant_id   = rs.variant_id
                detail.amount       = rs.amount
                detail.save()

            # payment_option = form.cleaned_data.get('payment_option')

            # if payment_option == 'S':
            #     return redirect('order:payment', payment_option='stripe')
            # elif payment_option == 'P':
            #     return redirect('order:payment', payment_option='paypal')
            # else:
            #     messages.warning(self.request, "Invalid payment option selected")
            #     return redirect('order:checkout')

            messages.success(self.request, "Your Order has submitted, now please complete the payment ")
            return redirect('order:razor')

        else:
            # messages.warning(self.request, "Your order not submited")
            messages.warning(self.request, form.errors)
            return redirect("order:checkout")

  


class PaymentView(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        category = Category.objects.all()
        order = Order.objects.filter(user=self.request.user, ordered=False)
        for order in order:
            print(order.total, 'price to prints ....')

        total = int(order.total *100)

        if order.billing_address:
        
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'category':category,
                
            }
            return render(self.request, "pay.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("order:payment")




@login_required(login_url ='/register/customer_login/') # Check login
def user_orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id, ordered=True).order_by('-id')
    context = {
               'category': category,
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)



@login_required(login_url ='/register/customer_login/') # Check login
def user_orderdetail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)

    orderitems = OrderProduct.objects.filter(order_id=id)

    print("i want to see orderitem dude", orderitems)

    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)



@login_required(login_url ='/register/customer_login/') # Check login
def user_order_product(request):
    #category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {#'category': category,
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)


@login_required(login_url ='/register/customer_login/') # Check login
def user_order_product_detail(request,id,oid):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'dash-manage-order.html', context)


