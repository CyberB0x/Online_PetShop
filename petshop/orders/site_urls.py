from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_view, name="cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", views.update_cart, name="update_cart"),
    path("remove/<int:item_id>/", views.remove_item, name="remove_item"),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='orders_list'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]
