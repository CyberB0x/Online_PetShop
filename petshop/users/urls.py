from django.urls import path
from .views import register, user_login, user_logout

urlpatterns = [
    path("register/", register),
    path("login/", user_login),
    path("logout/", user_logout),
]