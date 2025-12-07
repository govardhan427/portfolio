# backend/blog/views.py

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides public read access to published BlogPosts via slug.
    (Inherits list and retrieve methods only, blocking POST, PUT, DELETE for security)
    """
    # Only show published posts to the world
    queryset = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny] 
    
    lookup_field = 'slug'
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
class BlogManagementViewSet(viewsets.ModelViewSet):
    """Allows administrators to create, update, and delete ALL blog posts."""
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser] 
    lookup_field = 'slug'