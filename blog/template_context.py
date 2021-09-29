from .models import Blog_Category, Post
from products.models import Category
from django.db.models import Count
from django.db.models.aggregates import Max, Min, Count

def get_filters(request):

    category = Category.objects.all()
    blog_category = Blog_Category.objects.all()
    recent = Post.objects.filter(featured=True)
    tags = Post.tags.all()


    # shop= Product.objects.distinct().values('shop__name', 'shop__id').annotate(shop_count=Count('shop'))
    
    # color = Variants.objects.distinct().values('color__name', 'color__id', 'color__code').annotate(color_count=Count('color'))
    # size = Variants.objects.distinct().values('size__code', 'size__id').annotate(size_count=Count('size'))
    # minMaxPrice=Variants.objects.aggregate(Min('price'),Max('price'))

    # current_user = request.user
    #  # Access User Session information
    # shopcart = ShopCart.objects.filter(user_id=current_user.id)
    # order_count = Order.objects.filter(user_id=current_user.id, ordered=True)
    # order_canceld = Order.objects.filter(user_id=current_user.id, ordered=True, status='Canceled').count()

    data = {

        'category':category,
        'blog_category':blog_category,
        'recent_post':recent,
        'tags':tags,

    }
    
    return data