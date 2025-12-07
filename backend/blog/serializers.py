# backend/blog/serializers.py

from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    # CRITICAL FIX: Explicitly define the image field to generate the full Cloudinary URL
    cover_image = serializers.ImageField(read_only=True) 

    class Meta:
        model = BlogPost
        fields = '__all__'