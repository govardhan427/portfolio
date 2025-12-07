# backend/core/serializers.py

from rest_framework import serializers
from .models import Skill, Project, ProjectImage, Certificate, Journey, Achievement

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'proficiency', 'icon_class']

class ProjectImageSerializer(serializers.ModelSerializer):
    # CRITICAL CHANGE 1: Remove custom ImageField and rely on the model's new URLField name
    # The field will automatically be serialized as a string URL.
    
    class Meta:
        model = ProjectImage
        # CRITICAL CHANGE 2: Use the new field name: 'image_url'
        fields = ['id', 'image_url', 'caption', 'is_feature'] 

class ProjectSerializer(serializers.ModelSerializer):
    # Nested Serializers: Include the full skill and image objects, not just IDs
    skills = SkillSerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'tagline', 'description', 
            'skills', 'images', 'demo_link', 'github_link', 
            'featured_image_url', # CRITICAL CHANGE 3: Include the new featured image URL field
            'featured', 'created_at'
        ]

class CertificateSerializer(serializers.ModelSerializer):
    # CRITICAL CHANGE 4: The Certificate model's image field was also renamed to 'image_url'
    
    class Meta:
        model = Certificate
        # We assume you want to include all fields, so we rely on the model definition for the name 'image_url'
        fields = '__all__' 

class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'