# backend/blog/views.py

from rest_framework import viewsets, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.permissions import AllowAny, IsAdminUser # Ensure IsAdminUser is imported if needed

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet): # CHANGED to ReadOnlyModelViewSet for security
    """
    Provides public read access to published BlogPosts via slug.
    (Inherits list and retrieve methods only, blocking POST, PUT, DELETE for security)
    """
    # Only show published posts to the world
    queryset = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = BlogPostSerializer
    
    # Allow anyone to read the published posts
    permission_classes = [permissions.AllowAny] 
    
    lookup_field = 'slug'
    
    # --- CRITICAL FOR IMAGE FIX ---
    # Inject the request object into the serializer for absolute Cloudinary URL generation
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context