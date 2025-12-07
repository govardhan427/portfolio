# backend/blog/serializers.py

from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(read_only=True)
    class Meta:
        model = BlogPost
        fields = [
            'id', 
            'title', 
            'slug', 
            'content', 
            'cover_image', 
            'tags', 
            'is_published', 
            'created_at', 
            'read_time'
        ]