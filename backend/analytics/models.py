import uuid
from django.db import models

class Visitor(models.Model):
    # We use UUID so visitors can't guess ID sequence (e.g., visitor #5)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Identification
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(help_text="Browser/OS Details")
    
    # Derived Data (We fill this via logic later)
    device_type = models.CharField(max_length=20, default='Desktop') # Mobile/Tablet/Desktop
    location = models.JSONField(default=dict, blank=True) # {city: 'Mumbai', country: 'India'}
    
    # Timing
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ip_address} ({self.first_visit.strftime('%Y-%m-%d')})"

class PageView(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='page_views')
    path = models.CharField(max_length=255, help_text="The URL they visited")
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10, default='GET') # GET, POST
    
    # Metadata
    referrer = models.CharField(max_length=500, blank=True, null=True, help_text="Where did they come from?")
    status_code = models.IntegerField(default=200)

    class Meta:
        ordering = ['-timestamp'] # Show newest first

    def __str__(self):
        return f"{self.path} at {self.timestamp}"