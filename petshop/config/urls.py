from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home + продукты (главная и корзина)
    path("", include('products.urls')),
    path("", include("users.site_urls")),
    path("orders/", include("orders.frontend_urls")),


    # API endpoints
    path("api/orders/", include("orders.urls")),
    # path('api/payments/', include('payments.urls')),
    # path('api/reviews/', include('reviews.urls')),
    path("api/users/", include("users.urls")),

    # JWT токены
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)