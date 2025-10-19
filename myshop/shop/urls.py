from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),

    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    path('product/<slug:slug>/review/', views.add_review, name='add_review'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]