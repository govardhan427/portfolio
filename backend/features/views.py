from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from .ai_chat import get_smart_response
from .image_generator import generate_project_og
from .steganography import encode_text_into_image
import time
import os
from django.db import connection


class AIChatView(APIView):
    """
    Endpoint: POST /api/v1/features/chat/
    Body: { "query": "What did he build?" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        query = request.data.get('query', '')
        response_data = get_smart_response(query)
        return Response(response_data)

class OGImageView(APIView):
    """
    Endpoint: GET /api/v1/features/og-image/?title=MyProject&tagline=CoolApp
    """
    permission_classes = [AllowAny]

    def get(self, request):
        title = request.GET.get('title', 'Govardhan')
        tagline = request.GET.get('tagline', 'Full Stack Developer')
        
        image_bytes = generate_project_og(title, tagline)
        
        return HttpResponse(image_bytes, content_type="image/png")

class SteganographyView(APIView):
    """
    Endpoint: POST /api/v1/features/hide-text/
    Flex feature: Uploads an image and a text, returns the image with hidden text.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        image_file = request.FILES.get('image')
        secret_text = request.data.get('text', 'Secret Resume')

        if not image_file:
            return Response({"error": "No image provided"}, status=400)

        # Process logic
        processed_image = encode_text_into_image(image_file, secret_text)
        
        response = HttpResponse(processed_image, content_type="image/png")
        response['Content-Disposition'] = 'attachment; filename="hidden_secret.png"'
        return response
class SystemStatusView(APIView):
    """
    Real-time system health check.
    Calculates DB latency and reports server status.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Measure DB Latency
        start_time = time.time()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1") # Simple ping
            db_status = "Operational"
        except Exception:
            db_status = "Degraded"
        end_time = time.time()
        
        latency = (end_time - start_time) * 1000 # Convert to ms

        # 2. Get Uptime (Mocked for now, or use server start time)
        # In a real app, we'd store the start timestamp in apps.py
        
        return Response({
            "status": "Operational" if db_status == "Operational" else "Degraded",
            "database": db_status,
            "latency": f"{latency:.2f}ms",
            "region": "Mumbai (ap-south-1)", # Hardcode your deployment region
            "version": "v1.0.4", # You update this manually on deploy
            "commit": os.getenv("RENDER_GIT_COMMIT", "dev-build")[:7], # Render gives this env var
            "services": [
                {"name": "API Gateway", "status": "operational"},
                {"name": "File Vault (S3)", "status": "operational"},
                {"name": "Visitor Tracking", "status": "operational"},
            ]
        })