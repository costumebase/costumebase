from django.db.models.aggregates import Max, Min
import products
from django.shortcuts import redirect, render
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

import json
from .models import *
from cart.models import *


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
    template_name = 'land-page/landing.html'





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
        context['category'] = Category.objects.all()
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
    related_product = Product.objects.filter(category=product.category).exclude(id=id)[:15]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'product': product, 'related_product': related_product,
               'category': category,'images': images, 'comments': comments,
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
                        'variant': variant,'query': query
                        })
                        
    return render(request,'product-detail-variable.html',context)

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




