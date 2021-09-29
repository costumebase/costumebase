from django.urls import path 

from .import views

app_name = 'product'

urlpatterns = [


   
    path('', views.LandingPage.as_view(), name='index'),

    path('products/', views.Product_Index.as_view(), name='product-index'),
    # path('product-detail/<slug>/',views.Product_Detail.as_view(), name='product-detail'),
    path('add_to_wish/<int:id>/', views.add_to_wish, name ='add_to_wish'),

    path('product-detail/<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),

    


    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),

    path('addcomment/<int:id>/', views.addcomment, name='addcomment'),


    path('category/<slug>/', views.Category_Detail.as_view(), name='category-detail'),


   
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    path('auto/', views.auto, name='auto'),


    # Wishlist

    path('wish/', views.Wish_View.as_view(), name='wish'),
    path('delete_wish_item/<int:id>/', views.delete_wish_item, name='delete_wish_item'),



    # Shop
    path('shops/', views.Shops.as_view(), name='shops'),
    path('free-shipping/', views.Free_Shipping.as_view(), name='free-shipping'),

    # Filter
    path('filterMdata/',views.filter_data, name='filter_data'),
    path('product-list/', views.Product_List.as_view(), name='product-list'),


    # Message

    path('send-message/<int:id>/<str:name>/',views.send_massage, name='send-message'),

    # path('product-detail-message/<int:id>/', views.massage, name='product-detail-message'),

    # path('detail/', views.)

    path("messages/", views.index, name="index"),

    path("message_search/", views.search, name="message_search"),

    path("addfriend/<str:name>", views.addFriend, name="addFriend"),
    
    path("chat/<str:username>", views.chat, name="chat"),
    
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
   

]