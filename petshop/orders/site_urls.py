from django.urls import path
from . import site_views

urlpatterns = [
    path('cart/', site_views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', site_views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', site_views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', site_views.checkout_view, name='checkout'),
    path('', site_views.my_orders, name='orders_list'),  # /orders/
]
