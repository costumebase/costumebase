from django.urls import path 

from .import views

app_name = 'order'

urlpatterns = [
    

    
    path('checkout/', views.Checkout.as_view(), name='checkout'),

    path('payment/', views.PaymentView.as_view(), name='payment'),

    path('razor/', views.razor, name='razor'),
    path('success/',views.payment_success, name="payment-success"),



    path('checkoutt/', views.checkoutt.as_view(), name='chekcoutt'),

    # path('orderproduct/', views.orderproduct, name='orderproduct'),

    path('user-order/', views.user_orders, name='user-order'),

    path('orderdetail/<int:id>', views.user_orderdetail, name='user-orderdetail'),

    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),







] 