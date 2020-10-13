"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("home/", views.homepage, name="home"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("activation/", views.activation, name="activation"),
    path("purchase/", views.purchase, name="purchase"),
    path("orders/", views.orders, name="orders"),
    path("getcartitems/", views.get_cart_items, name="getcartitems"),
    path("item/<int:pk>", views.item_view, name="item_view"),


    
    path("cart/", views.cart, name="cart"),
]
