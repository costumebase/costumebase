from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse, request
from django.shortcuts import get_list_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import generic
from order.models import *
from products.models import *
from products.models import Category, Product

from .decorators import vendor_required
from .forms import *
from .models import Friends, Messages, Vendor_Payment
from .utilits import (colorDanger, colorPrimary, colorSuccess,
                      generate_color_palette, get_year_dict, months)

""" ................................................ Vendor Dashboard ............................................. """

# @method_decorator([login_required, vendor_required], name='dispatch')

@login_required(login_url='/register/vendor_login/') 
@vendor_required
def dashboard(request):
    orderproduct = OrderProduct.objects.filter(vendor=request.user.vendor, status='Delivered')
    neworder = OrderProduct.objects.filter(vendor=request.user.vendor, status='New')
    totalorder = OrderProduct.objects.filter(vendor=request.user.vendor)
    totalproduct = Product.objects.filter(vendor=request.user.vendor, is_for_sale='True').count()

    print(totalproduct, " let's print total producto of this vendor")
    
    total = 0
    for i in orderproduct:  
        bar1 = i.product.vendor
        if i.variant and i.product:
            total += i.variant_amount
        else:
            total += i.amount
        payment = Vendor_Payment()
        if i.product.vendor == request.user.vendor:
            payment.vendor = i.product.vendor
            payment.vendor_paid_total = total
            payment.save()                   # delter old reload page
    return render(request, 'board_index.html', {'total':total, 'orderproduct':orderproduct, 'totalorder':totalorder,
                                              'neworder':neworder, 'totalproduct':totalproduct})


class Delivered_Product_list(generic.ListView):
    model = OrderProduct
    template_name = 'delivered_product_list.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        return self.model.objects.filter(vendor=self.request.user.vendor, status='Delivered')


class Detail_Delivered_Product(generic.DetailView):
    model = OrderProduct
    template_name = 'detail_delivered_product.html'
    context_object_name = 'queryset'


class New_Order_list(generic.ListView):
    model = OrderProduct
    template_name = 'new_order_list.html' 
    context_object_name = 'queryset'

    def get_queryset(self):
        return self.model.objects.filter(vendor=self.request.user.vendor, status='New')


class Detail_New_Order(generic.DetailView):
    model = OrderProduct
    template_name = 'detail_new_list.html'
    context_object_name = 'queryset'



class Total_Order(generic.ListView):
    model = OrderProduct
    template_name = 'total_order_list.html' 
    context_object_name = 'queryset'

    def get_queryset(self):
        return self.model.objects.filter(vendor=self.request.user.vendor)


class Detail_Total_Order(generic.DetailView):
    model = OrderProduct
    template_name = 'detail_total_list.html'
    context_object_name = 'queryset'





class Chart(generic.TemplateView):
    template_name = 'charts.html'

class Product_List(generic.ListView):
    model = Product
    template_name = 'product-list.html'
    context_object_name = 'queryset'

    def get_queryset(self):
    
        return self.model.objects.filter(vendor=self.request.user.vendor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


    
class Add_Product(generic.CreateView):
    model = Product
    template_name = 'add_product.html'
    form_class = ProductCreateForm
    success_url = 'dashboard/add-product'

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        form.instance.slug = slugify(form.instance.name)
        form.save()
        return redirect(reverse("dashboard:add-product"))
   
    # def get_context_data(self, **kwargs):
    #     self.profile = Adm_Profile.objects.all()
    #     context = super().get_context_data(**kwargs)
    #     context['profile'] = self.profile
    #     return context



def add_image(request):
    current = request.user.vendor
    productb = Product.objects.filter(vendor=current)
    print("hey man i am habving trouble", productb)
    if request.method == "POST":
        form = ImageCreateForm(request.POST, request.FILES)
        if form.is_valid():

            current = request.user.vendor
            products = form.cleaned_data['product']
            name = form.cleaned_data['name'] #variable to store cleaned data
            image = form.cleaned_data['image'] 
            instance = Images(vendor=current, product=products, name=name, image=image)
            instance.save()
            # print("hello user", form.user)
        else:
            print("i am use less")
    else:
        form = ImageCreateForm()
    return render(request, 'add_image.html', {'form': form, 'productb':productb})


class Image_list(generic.ListView):
    model = Images
    template_name = 'image_list.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        return self.model.objects.filter(vendor=self.request.user.vendor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    
def add_product_variation(request):
    current = request.user.vendor
    productby = Product.objects.filter(vendor=current)

    colorby = Color.objects.all()

    if request.method == "POST":
        form = ProductVariation(request.POST, request.FILES)
        if form.is_valid():

            current = request.user.vendor
         
            name = form.cleaned_data['name']    
            product = form.cleaned_data['product']
            color = form.cleaned_data['color']
            size = form.cleaned_data['size']
            image_id = form.cleaned_data['image_id']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']

            instance = Variants(vendor=current, name=name, product=product, color=color, size=size, 
                            image_id=image_id, quantity=quantity, price=price)
            instance.save()

        else:
            print("i am use less")
    else:
        form = ProductVariation()
    return render(request, 'add_variant.html', {'form': form, 'product':productby, 'color':colorby})



# def new_animal(request):

#     if request.method == "POST":
#         form = ProductCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.user = request.user.vendor
#             print("hello user", form.user)
#             form.save()
#         else:
#             print("i am use less")
#     else:
        
#         form = ProductCreateForm()
#     return render(request, 'add_product.html', {'form': form})


from products.views import getUserId, getFriendsList

def vendor_chat(request, username):
    """
     Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    friend = User.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = User.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        return render(request, "chat/vendor_messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})





#............................... Chart ...................................#







def pie_chart(request):

    return render(request, 'pie.html')

def population_chart(request):  
                   #chart by
    labels = []
    data = []

    product = Product.objects.all()

    for p in product:
        pp = p.name
        pd = p.price
        labels.append(pp)
        data.append(pd)


    return JsonResponse(data={
        'labels': labels,
        'data':data,
    })





def get_filter_options(request):
    grouped_purchases = OrderProduct.objects.annotate(year=ExtractYear('create_at')).values('year').order_by('-year').distinct()
    options = [purchase['year'] for purchase in grouped_purchases]

    return JsonResponse({
        'options': options,
    })



def get_sales_chart(request):
    purchases = Vendor_Payment.objects.filter()


   


    return JsonResponse({
        

       
    })











# ----------------------------- User Dashboard -------------------------------


class Customer_Profile(generic.ListView):
    model = Buyer
    template_name = 'dash-my-profile.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class User_Dashboard(generic.ListView):
    model = Order
    template_name = 'user_dashboard.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['profile'] = Buyer.objects.filter(user=self.request.user)

        context['category'] = Category.objects.all()
        return context



class User_Order(generic.ListView):
    model = Order
    template_name = 'dash-my-order.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = Category.objects.all()

        return context

#................................................ Message .................................................


class User_Message(generic.ListView):
    model = Messages
    template_name = 'message_user.html'
    context_object_name = 'chat'



class Message_Detail(generic.DetailView):
    model = Messages
    template_name = 'message_user.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = self.request.path
        context['active'] = 'active'
        return context
  


    