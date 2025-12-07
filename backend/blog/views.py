# backend/blog/views.py

from rest_framework import viewsets, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.permissions import AllowAny

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides public read access to published BlogPosts via slug.
    ReadOnlyModelViewSet ensures no public POST/PUT/DELETE access.
    """
    # NOTE: This line is correct, but needs the database fields to exist.
    queryset = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny] 
    lookup_field = 'slug'
    
    # --- CRITICAL FOR IMAGE FIX ---
    # Inject the request object into the serializer for absolute Cloudinary URL generation
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context