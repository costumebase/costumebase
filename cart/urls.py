from django.urls import path 

from .import views

app_name = 'cart'

urlpatterns = [
    

    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),

    path('shopcart/', views.shopcart, name='shopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),

    path('add-cart/<int:id>/', views.add_one_product, name='addcart'),
    path('remove-cart/<int:id>/', views.remove_one_product, name='romovecart'),



    path('remove_variant_product/<int:id>/', views.remove_variant_product, name='remove_variant_product'),
    path('add_variant_product/<int:id>/', views.add_variant_product, name='add_variant_product'),





    # path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),


  




] 