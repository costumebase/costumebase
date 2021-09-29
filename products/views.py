from django import forms
from django.db.models.aggregates import Max, Min
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.contrib import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, query
from itertools import chain, product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from .models import *
from order.models import OrderProduct
from cart.models import *
from .forms import MessageForm

# def shopcartcount(userid):
#     count = ShopCart.objects.filter(user_id=userid).count()
#     print('')
#     return count

class SearchView(generic.ListView):
    model = Product
    template_name = 'search_list.html'    
    paginate_by = 2
    # context_object_name = 'object_list'

    def get_queryset(self, *args, **kwargs):
            # qs = super().get_queryset(*args, **kwargs)
            product = Product.objects.all()
            # shop = Shop.objects.all()
            query = self.request.GET.get('q')

            if query:

                product = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query)).distinct()
                # queryset = Shop.objects.filter(Q(name__icontains=query)|Q(discription__icontains=query)).distinct()

                # queryset = list(
                #     sorted(
                #         chain(product),
                #         key=lambda objects: objects.pk
                #     ))
            return product
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context
    


def auto(request):
    query = request.GET.get('term')
    product = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query)).distinct()
    # queryset = Shop.objects.filter(Q(name__icontains=query)|Q(discription__icontains=query)).distinct()
    # autoo = chain(queryset, product)
    mylist = []
    mylist += [x.name for x in product]
    return JsonResponse(mylist, safe=False)


class LandingPage(generic.TemplateView):
    template_name = 'message_user.html'





class Product_Index(generic.ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'queryset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['recent'] = Product.objects.filter(is_for_sale=True).order_by('-created_at')[0:15]

        context['cart'] = ShopCart.objects.filter(user_id=current_user.id)

        context['variant'] = Variants.objects.all() 
        context['topcat'] = Category.objects.filter(top_category=True)[:7]
        print( context['topcat'] )
        return context



# class Product_Detail(generic.DetailView):
#     model = Product
#     template_name = 'product-detail-variable.html'
#     context_object_name = 'queryset'

#     def get_queryset(self):
#         return super().get_queryset() 

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category'] = Category.objects.all()
#         return context


def product_detail(request,id,slug):
    query = request.GET.get('q')
    
    category = Category.objects.all()

    product = Product.objects.get(pk=id)

    vendor_message = product.vendor.user.username
    message_user = list(User.objects.all())

    for user in message_user:
        if user.username == request.user.username:
            message_user.remove(user)
            break
    try:
        message_user = message_user[:10]
    except:
        message_user = message_user[:]

    bar = 0
    sold_product = OrderProduct.objects.filter(product_id=id)
    for i in sold_product:
        bar += i.quantity
   
    related_product = Product.objects.filter(category=product.category).exclude(id=id)[:15]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    
    wish_count =  Wishlist.objects.filter(product_id=id).count()



    context = {'product': product, 'related_product': related_product, 'bar':bar,
               'category': category,'images': images, 'comments': comments,
                'message_user':message_user, 'vendor':vendor_message,'wish_count':wish_count,
               }

    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.name+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)



        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query,})
                        
    return render(request,'product-detail-variable.html',context)




@login_required(login_url='/register/customer_login/')
def add_to_wish(request, id):
    item = get_object_or_404(Product, id=id)
    wish_item, created = Wishlist.objects.get_or_create(
        product=item,
        user=request.user
    )
    
    if created:
        messages.info(request, "item added to your wish")
    else:
        messages.warning(request, "item was alrady in your wish")
    return redirect('product:product-index')



@login_required(login_url='/register/customer_login/')
def delete_wish_item(request, id):
    item = get_object_or_404(Product, id=id)
    wish_item = Wishlist.objects.filter(product=item, user=request.user).delete()
    messages.info(request, "item just deleted from your wishlist")
    return redirect('product:wish')



from django.utils.decorators import method_decorator
from .decorators import customer_required


@method_decorator([login_required, customer_required], name='dispatch')
class Wish_View(generic.ListView):
    model = Wishlist
    template_name = 'wish.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['wish_view'] = self.model.objects.filter(user_id=current_user.id)
        context['cart'] = ShopCart.objects.filter(user_id=current_user.id)
        context['variant'] = Variants.objects.all() 
        context['topcat'] = Category.objects.filter(top_category=True)[:7]
        print( context['topcat'] )
        return context




def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)



# @login_required(login_url='/register/customer_login/')
@customer_required
def addcomment(request, id):
   url = request.META.get('HTTP_REFERER')  # get last url
   current_user= request.user.buyer
   print(current_user, "lasjdflajsfdlajsdfl")
   #return HttpResponse(url)
   product = Product.objects.get(id=id)
   print(product.id, "lolllllll")
   form = CommentForm(request.POST or None)
   if request.method == 'POST':  # check post
       
       if form.is_valid():
           data = Comment()  # create relation with model
           data.name = form.cleaned_data['name']
           data.subject = form.cleaned_data['subject']
           data.comment = form.cleaned_data['comment']
           data.rate = form.cleaned_data['rate']
           data.ip = request.META.get('REMOTE_ADDR')
           data.product_id=product.id
           print(current_user, "fuck yes")
           data.user=current_user
           data.save()  # save data to table
           messages.success(request, "Your review has ben sent. Thank you for your interest.")
           return redirect('product:product-detail', id=product.id, slug=product.slug)

   return render(request, "comment.html", {'form':form, 'product':product})

class Category_Detail(generic.DetailView, MultipleObjectMixin):
    model = Category
    template_name = 'category-grid-left.html'
    paginate_by = 2
    # context_object_name = 'data'

    def get_context_data(self, **kwargs):
        object_list = Product.objects.filter(category=self.object)
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category'] = Category.objects.all()
        return context

class Shops(generic.ListView):
    model = Shop
    template_name = 'shop-list-full.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_count'] = Shop.objects.all().count()
        context['category'] = Category.objects.all()
        return context
                
class Shop_Detail(generic.DetailView, MultipleObjectMixin):
    model = Shop
    template_name = 'shop-gird-left.html'
    context_object_name = 'queryset'
    paginate_by = 1
    
    def get_context_data(self, **kwargs):
        object_list = Product.objects.filter(category=self.object)
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category'] = Category.objects.all()
        return context

class Free_Shipping(generic.ListView):
    model = Product
    template_name = 'category-grid-left.html'
    context_object_name = 'queryset'
    paginate_by= 1

    def get_context_data(self, **kwargs):
        object_list = Product.objects.filter(is_free_shipping=True)
        query = 'FREE SHIPPING PRODUCTS'
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category'] = Category.objects.all()
        context['query'] = query
        return context


class Product_List(generic.ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'object_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] = Product.objects.filter(is_for_sale=True).order_by('-created_at')[0:15]
        context['variant'] = Variants.objects.all() 
        context['category'] = Category.objects.all()
        return context


def filter_data(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	shops=request.GET.getlist('shop[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=Product.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(variants__price__gte=minPrice)
	allProducts=allProducts.filter(variants__price__lte=maxPrice)

    
	if len(colors)>0:
		allProducts=allProducts.filter(variants__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(shops)>0:
		allProducts=allProducts.filter(shop__id__in=shops).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(variants__size__id__in=sizes).distinct()
	t=render_to_string('ajax/product-list.html',{'object_list':allProducts})
	return JsonResponse({'object_list':t})

# def filter_data(request):
#     return JsonResponse({'data':'hello'})




from dashboard.models import Messages
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from products.serializers import MessageSerializer


def getFriendsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user = User.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = User.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    """
    Get the user id by the username
    :param username:
    :return: int
    """
    use = User.objects.get(username=username)
    id = use.id
    return id


def index(request):
    """
    Return the home page
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        username = request.user.username
        id = getUserId(username)
        friends = getFriendsList(id)
        return render(request, "chat/Base.html", {'friends': friends})


def search(request):
    """
    Search users page
    :param request:
    :return:
    """
    message_user = list(User.objects.all())

    for user in message_user:
        if user.username == request.user.username:
            message_user.remove(user)
            break
    try:
        message_user = message_user[:10]
    except:
        message_user = message_user[:]
        

    # if request.method == "POST":
    #     print("SEARCHING!!")
    #     query = request.POST.get("search")
    #     user_ls = []
    #     for user in users:
    #         if query in user.name or query in user.username:
    #             user_ls.append(user)

                
    #     return render(request, "chat/search.html", {'users': user_ls, })

    id = getUserId(request.user.username)
    friends = getFriendsList(id)

    return render(request, "chat/search.html", {'users': message_user, 'friends': friends})


def addFriend(request, name):
    """
    Add a user to the friend's list
    :param request:
    :param name:
    :return:
    """
    username = request.user.username
    id = getUserId(username)
    friend = User.objects.get(username=name)
    curr_user = User.objects.get(id=id)
    print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0

    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break

    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)


    return redirect("/search")

@customer_required
def chat(request, username):
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
        return render(request, "chat/messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



@customer_required
def send_massage(request, id, name):
    # if this is a POST request we need to process the form data
    url = request.META.get('HTTP_REFERER')  # get last url

    product = Product.objects.get(pk=id)   
    url = request.path
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MessageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = Messages()
            data.sender_name = request.user
            data.receiver_name =  product.vendor.user
            # data.url = url
            data.description = form.cleaned_data['description']
            data.save()

            username = request.user.username
            id = getUserId(username)
            friend = User.objects.get(username=name)
            curr_user = User.objects.get(id=id)
            print(curr_user.name)
            ls = curr_user.friends_set.all()
            flag = 0

            for username in ls:
                if username.friend == friend.id:
                    flag = 1
                    break

            if flag == 0:
                print("Friend Added!!")
                curr_user.friends_set.create(friend=friend.id)
                friend.friends_set.create(friend=id)
            # form.save()
            messages.success(request, "Your Message has ben sent. Thank you!")
            return redirect('product:product-detail', id=product.id, slug=product.slug)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MessageForm()

    return render(request, 'message.html', {'form': form, 'product':product,})

