from django.urls import path
from .views import orders_page

urlpatterns = [
    path("", orders_page, name="orders_page"),
]
