from rest_framework import serializers
from .models import Skill, Project, ProjectImage, Certificate, Journey, Achievement

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'proficiency', 'icon_class']

class ProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'is_feature']

class ProjectSerializer(serializers.ModelSerializer):
    # Nested Serializers: Include the full skill and image objects, not just IDs
    skills = SkillSerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'tagline', 'description', 
            'skills', 'images', 'demo_link', 'github_link', 
            'featured', 'created_at'
        ]

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'
class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'