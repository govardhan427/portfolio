# backend/blog/serializers.py

from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    # CRITICAL CHANGE: The field name changes from 'cover_image' to 'cover_image_url'
    # No custom ImageField required here, it uses the standard ModelSerializer field.

    class Meta:
        model = BlogPost
        # Ensure the new field name is listed
        fields = ('id', 'title', 'slug', 'content', 'cover_image_url', 'tags', 'is_published', 'created_at', 'read_time')