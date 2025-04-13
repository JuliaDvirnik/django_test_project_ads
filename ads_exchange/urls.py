"""ads_exchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from ads.views import create_ad, ad_detail, register, ad_list, delete_ad, edit_ad, create_exchange, exchange_detail, my_exchanges

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ad_list, name='index'),
    path('ads/create/', create_ad, name='create_ad'),
    path('ads/<int:pk>/', ad_detail, name='ad_detail'),
    path('ads/<int:pk>/delete/', delete_ad, name='delete_ad'),
    path('ads/<int:pk>/edit/', edit_ad, name='edit_ad'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', register, name='register'),
    path('exchange/', create_exchange, name='create_exchange'),
    path('exchange/<int:pk>/', exchange_detail, name='exchange_detail'),
    path('my-exchanges/', my_exchanges, name='my_exchanges'),
]