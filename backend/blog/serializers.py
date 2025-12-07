# backend/blog/serializers.py

from rest_framework import serializers
from .models import BlogPost
import cloudinary

class BlogPostSerializer(serializers.ModelSerializer):
    # CRITICAL FIX: Use SerializerMethodField to construct the absolute URL template
    cover_image_url = serializers.SerializerMethodField() 
    
    class Meta:
        model = BlogPost
        # Include the new field and exclude the original FileField
        fields = ('id', 'title', 'slug', 'content', 'cover_image_url', 'tags', 'is_published', 'created_at', 'read_time')
    def get_cover_image_url(self, obj):
        if not obj.cover_image:
            return None
        
        # The file field's .name property holds the Cloudinary Public ID (e.g., 'blog_files/filename.jpg')
        public_id = obj.cover_image.name
        
        # This uses the Cloudinary utility method to generate the full, correct URL 
        # including version number, transformation, and resource type, bypassing all local conflicts.
        return cloudinary.utils.cloudinary_url(public_id, resource_type="image", secure=True)[0]