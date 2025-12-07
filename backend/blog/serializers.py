# backend/blog/serializers.py

from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    # CRITICAL FIX for Cloudinary: 
    # Define the image field explicitly to ensure DRF uses the file's .url property,
    # which resolves to the absolute Cloudinary URL when the request context is passed.
    cover_image = serializers.ImageField(read_only=True) 

    class Meta:
        model = BlogPost
        # Use '__all__' or define the list of fields explicitly
        fields = '__all__'