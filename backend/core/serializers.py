from rest_framework import serializers
from .models import Skill, Project, ProjectImage, Certificate, Journey, Achievement
from django.conf import settings # Needed for generating absolute URLs

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'proficiency', 'icon_class']

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        # CRITICAL CHANGE 2: Use the new field name: 'image_url'
        fields = ['id', 'image_url', 'caption', 'is_feature'] 

class ProjectSerializer(serializers.ModelSerializer):
    # Nested Serializers
    skills = SkillSerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    # CRITICAL FIX 1: Define the og_image_url field as a SerializerMethodField
    og_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'tagline', 'description', 
            'skills', 'images', 'demo_link', 'github_link', 
            'featured_image_url',       # CRITICAL CHANGE 3: New URL field
            'og_image_url',             # CRITICAL FIX 2: Include the generated image URL
            'featured', 'created_at'
        ]

    # CRITICAL FIX 3: Method to generate the absolute URL for the generated image
    def get_og_image_url(self, obj):
        request = self.context.get('request')
        # Check if the file exists and the request context is available
        if obj.og_image and request:
            # Use request.build_absolute_uri to get the full public URL
            return request.build_absolute_uri(obj.og_image.url)
        return None


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        # CRITICAL FIX 4: Explicitly list fields for safety post-migration
        fields = (
            'id', 'name', 'issuer', 'date_issued', 
            'credential_url', 'image_url' # Ensure image_url is the name used
        ) 

class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'