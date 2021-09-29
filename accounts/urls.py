

from os import name
from products import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (customer_register, vendor_register, account_activation_sent,
                Vendor_Registration_Index, auth_view, sms_verify)




from .active import activate, activate_customer

app_name = 'register'

urlpatterns = [

    

    path('vendor_login/', auth_view, name='vendor_login'),
    path('vendor_register/', vendor_register, name='vendor_register'),
    path('verify/', sms_verify, name='verify'),





    path('', Vendor_Registration_Index.as_view(), name='vendor_registration_index'),

    # path('login/', .as_view(), name='signup'),
    # path('vendor/signup/', VendorSignUpView.as_view(), name='ven_signup'), 

    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', activate, name='active'),

    path('active_customer/<uidb64>/<token>/', activate_customer, name='active_customer'),


    path('customer_register/', customer_register, name='customer_register'),
    path('customer_login/', auth_views.LoginView.as_view(), name='customer_login'),
    path('customer_logout/', auth_views.LogoutView.as_view()),
    

    
    # path('password_change/', auth_views.PasswordChangeView.as_view()),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view()),
    # path('password_reset/', auth_views.PasswordResetView.as_view()),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view()),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view()),
    # path('reset/done/', auth_views.PasswordResetDoneView.as_view()),

    



]

# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']