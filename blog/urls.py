from django.urls import path 

from .import views

app_name = 'blog'

urlpatterns = [
    

    path('', views.BlogView.as_view(), name='blogview'),

    path('<slug>/', views.BlogDetail.as_view(), name='blogdetail'),

    path('search/', views.SearchView.as_view(), name='search'),


] 