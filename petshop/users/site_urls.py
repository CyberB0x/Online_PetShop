from django.urls import path
from . import site_views

urlpatterns = [
    path('login/', site_views.login_view, name='login'),
    path('register/', site_views.register_view, name='register'),
    path('logout/', site_views.logout_view, name='logout'),
    path("profile/", site_views.profile_view, name="profile"),
]
