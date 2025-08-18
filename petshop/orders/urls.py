from django.urls import path
from .views import add_to_cart, remove_from_cart, checkout, my_orders

urlpatterns = [
    path("cart/add/", add_to_cart),
    path("cart/remove/", remove_from_cart),
    path("checkout/", checkout),
    path("my-orders/", my_orders),
]
