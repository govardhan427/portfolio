from rest_framework import viewsets, parsers, permissions
from .models import PrivateFile
from .serializers import PrivateFileSerializer

class PrivateFileViewSet(viewsets.ModelViewSet):
    queryset = PrivateFile.objects.all().order_by('-uploaded_at')
    serializer_class = PrivateFileSerializer
    
    # 🚨 CRITICAL: This tells Django "Expect Files, not just JSON"
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    # In production, set this to [permissions.IsAdminUser]
    permission_classes = [permissions.IsAdminUser]