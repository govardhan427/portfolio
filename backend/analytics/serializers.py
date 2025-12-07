from rest_framework import serializers
from .models import Visitor, PageView

class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = ['path', 'timestamp', 'method', 'referrer']

class VisitorSerializer(serializers.ModelSerializer):
    # Nested serializer to show the full journey
    page_views = PageViewSerializer(many=True, read_only=True)

    class Meta:
        model = Visitor
        fields = [
            'id', 'ip_address', 'device_type', 'location', 
            'user_agent', 'first_visit', 'last_visit', 'page_views'
        ]