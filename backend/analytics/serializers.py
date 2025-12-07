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
            'id', 
            'session_key',    # CRITICAL FIX 1: New field for session-based tracking
            'remote_ip',      # CRITICAL FIX 2: Corrected IP address field name
            'is_online',      # CRITICAL FIX 3: New field for online status
            'device_type', 
            'location', 
            'user_agent', 
            'first_visit', 
            'last_visit', 
            'page_views'
        ]