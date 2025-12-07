import uuid
from django.db import models

class Visitor(models.Model):
    # We use UUID for the internal primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # CRITICAL FIX 1: Field to store Django's session key for tracking continuity
    session_key = models.CharField(max_length=40, unique=True, null=True, blank=True)
    
    # CRITICAL FIX 2: Flag to mark user as active (managed by middleware/views)
    is_online = models.BooleanField(default=False) 
    
    # Identification
    remote_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(help_text="Browser/OS Details")
    
    # Derived Data
    device_type = models.CharField(max_length=20, default='Desktop') 
    location = models.JSONField(default=dict, blank=True) 
    
    # Timing
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now_add=True) 

    # CRITICAL FIX 4: Add this field to support the middleware logic
    visits = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.remote_ip} ({self.first_visit.strftime('%Y-%m-%d')})"

class PageView(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='page_views')
    path = models.CharField(max_length=255, help_text="The URL they visited")
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10, default='GET') 
    
    # Metadata
    referrer = models.CharField(max_length=500, blank=True, null=True, help_text="Where did they come from?")
    status_code = models.IntegerField(default=200)

    class Meta:
        ordering = ['-timestamp'] 

    def __str__(self):
        return f"{self.path} at {self.timestamp}"