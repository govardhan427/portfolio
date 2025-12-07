from django.urls import path
from .views import AIChatView, OGImageView, SteganographyView, SystemStatusView

urlpatterns = [
    path('chat/', AIChatView.as_view(), name='ai-chat'),
    path('og-image/', OGImageView.as_view(), name='og-image'),
    path('hide-text/', SteganographyView.as_view(), name='steganography'),
    path('status/', SystemStatusView.as_view(), name='system-status'),
]