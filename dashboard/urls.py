from django.urls import path 

from .import views

app_name = 'dashboard'

urlpatterns = [
    
 # ----------------------------------------- Vendor -------------------------------------

    path('index/', views.dashboard, name='index'),

    path('chart/', views.Chart.as_view(), name='chart'),

    path('add-product/', views.Add_Product.as_view(), name='add-product'),

    path('product-list/', views.Product_List.as_view(), name='product-list'),

    path('add-image/', views.add_image, name='add-image'),
    path('add-variant/', views.add_product_variation, name='add-varaint'),
    path('image-list/', views.Image_list.as_view(), name='image-list'),

    path('new-order/', views.New_Order_list.as_view(), name='new-order'),



    path('delivered-product-list/', views.Delivered_Product_list.as_view(), name='delivered-product-list'),
    path('detail-delivered-product/<int:pk>/', views.Detail_Delivered_Product.as_view(), name='detail-delivered-product'),

    #.......................................... Chart ........................................

    path('pie/', views.pie_chart, name = 'pie'),
    path('population-chart/', views.population_chart, name='population-chart'),
    path('chart/sales/<int:year>/', views.get_sales_chart, name='chart-sales'),

    




    # -------------------------------------- Customer -----------------------------------

    path('user-profile/', views.Customer_Profile.as_view(), name='user-profile'),
    path('user-dashboard/',views.User_Dashboard.as_view(), name='user-dashboard'),
    path('user-order/', views.User_Order.as_view(), name='user-order'),


    # ........................................ Message .................................

    path("chat/<str:username>", views.vendor_chat, name="vendor_chat"),


    path('user-message/', views.User_Message.as_view(), name='user-message'),

    path('message-detail/<int:pk>/', views.Message_Detail.as_view(), name='message_detail'),


    
]


