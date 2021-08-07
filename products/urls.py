from django.urls import path 

from .import views

app_name = 'product'

urlpatterns = [


   
    path('', views.LandingPage.as_view(), name='index'),

    path('products/', views.Product_Index.as_view(), name='product-index'),
    # path('product-detail/<slug>/',views.Product_Detail.as_view(), name='product-detail'),
    path('product-detail/<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),

    path('category/<slug>/', views.Category_Detail.as_view(), name='category-detail'),
   
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    path('auto/', views.auto, name='auto'),

    # Shop
    path('shops/', views.Shops.as_view(), name='shops'),
    path('free-shipping/', views.Free_Shipping.as_view(), name='free-shipping'),

    # Filter
    path('filterMdata/',views.filter_data, name='filter_data'),
    path('product-list/', views.Product_List.as_view(), name='product-list'),



    # path('detail/', views.)

   

]