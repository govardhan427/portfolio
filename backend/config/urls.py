from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Core API (Projects, Skills)
    path('api/v1/', include('core.urls')),
    
    # 2. Analytics API (Spy Mode)
    path('api/v1/analytics/', include('analytics.urls')),
    
    # 3. Vault API (Files)
    path('api/v1/vault/', include('vault.urls')),
    
    # 4. Blog API
    path('api/v1/blog/', include('blog.urls')),

    # 5. Authentication (Get Token)
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/features/', include('features.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)