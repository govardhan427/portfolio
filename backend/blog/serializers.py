# backend/blog/serializers.py

from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    # CRITICAL FIX: Use SerializerMethodField to get the absolute URL from the model property
    cover_image = serializers.ImageField(read_only=True) 
    class Meta:
        model = BlogPost
        # Change fields to include the new property and exclude the original FileField if necessary
        fields = '__all__'