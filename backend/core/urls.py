from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, SkillListView, HomeDataView, ContactAPIView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('home/', HomeDataView.as_view(), name='home-data'),
    path('contact/', ContactAPIView.as_view(), name='contact-form'),
]