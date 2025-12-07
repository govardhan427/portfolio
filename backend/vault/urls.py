from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrivateFileViewSet

router = DefaultRouter()
router.register(r'files', PrivateFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]