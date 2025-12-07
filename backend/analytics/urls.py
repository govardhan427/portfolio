from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackPageView, AnalyticsDashboardView, VisitorListView

router = DefaultRouter()
router.register(r'visitors', VisitorListView)

urlpatterns = [
    # React pings this on every route change
    path('track/', TrackPageView.as_view(), name='track-page'),
    
    # Admin dashboard fetches this to show graphs
    path('dashboard/', AnalyticsDashboardView.as_view(), name='dashboard-stats'),
    
    # List of individual visitors
    path('', include(router.urls)),
]