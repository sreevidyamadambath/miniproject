"""
URL configuration for secondproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from secondapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name="index"),
    path("home/",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("signup/",views.register,name="reg"),
    path("check_user/",views.check_user,name="check_user"),
    path("login/",views.user_login,name="log"),
    path("cust_dashboard/", views.cust_dashboard, name="cust_dashboard"),
    path("chef_dashboard/", views.chef_dashboard, name="chef_dashboard"),
    path("logout/", views.user_logout, name="logout"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("addproduct/",views.add_item_view,name="add_item_view"),
    path("my_products/",views.my_products,name="my_products"),
    path("viewitem/",views.viewitem,name="viewitem"),
    path("single_product/",views.single_product,name="single_product"),
    path("update_product/",views.update_product,name="update_product"),
    path("delete_product/",views.delete_product,name="delete_product"),
    path("all_products/", views.all_products, name="all_products"),
    path("cart/", views.add_to_cart, name="cart"),
    path("get_cart_data/", views.get_cart_data, name="get_cart_data"),
    path("change_quan/", views.change_quan, name="change_quan"),
    path('view_wallet/',views.view_wallet, name='view_wallet'),
    path('add_money/', views.add_money, name='add_money'),
    path('proceed_to_pay/',views.proceed_to_pay, name='proceed_to_pay'),
    path('order_history/',views.order_history, name='order_history'),
    path('chef_orders/',views.chef_orders, name='chef_orders'),
    path('search-chefs/', views.search_chefs, name='search_chefs'),
    path('all_chefs/', views.all_chefs, name='all_chefs'),
    path('update_order_status/<int:order_id>/',views.update_order_status, name='update_order_status'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
