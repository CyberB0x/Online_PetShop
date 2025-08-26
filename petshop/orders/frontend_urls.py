from django.urls import path
from .views import orders_page
from . import views

urlpatterns = [
    path("", orders_page, name="orders_page"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
]
