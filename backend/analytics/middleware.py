# backend/analytics/middleware.py

from django.utils import timezone
from datetime import timedelta
from .models import Visitor

ACTIVE_WINDOW_MINUTES = 5       # How long a user stays “online” after activity
MIN_UPDATE_INTERVAL = 30        # Only update DB every 30 sec (prevents spam)

# --- Utility to get IP (Integrated Logic) ---
def _get_client_ip(request):
    """Retrieves the real client IP address, handling proxy headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Note: User IP is the first IP in the list
        return x_forwarded_for.split(',')[0].strip() 
    else:
        return request.META.get('REMOTE_ADDR') or "0.0.0.0"


class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Skip admin, API paths that handle status, or paths without a session
        if request.path.startswith('/admin') or request.path.startswith('/api/v1/features/status/'):
            return self.get_response(request)

        # 1. Ensure session exists (CRITICAL: Required for session_key)
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        now = timezone.now()
        ip = _get_client_ip(request) # Use the proxy-aware IP retrieval

        # 2. Find or Create Visitor
        visitor, created = Visitor.objects.get_or_create(
            # Find by the session key
            session_key=session_key,
            defaults={
                # CRITICAL FIX: Use the proxy-aware IP
                "remote_ip": ip, 
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                # NOTE: Ensure 'visits' exists in models.py if setting default here
                "visits": 1, 
                "last_visit": now,
                "is_online": True
            }
        )
        
        # 3. Handle Updates for Existing Visitor
        if not created:
            # Check for minimum update interval for performance
            if visitor.last_visit < now - timedelta(seconds=MIN_UPDATE_INTERVAL):
                
                fields_to_update = ["last_visit", "is_online"]

                # New day check: increment visits
                if visitor.last_visit.date() < now.date():
                    visitor.visits += 1
                    fields_to_update.append("visits")
                
                # CRITICAL INTEGRITY FIX: Update IP if it changed mid-session
                if visitor.remote_ip != ip:
                    visitor.remote_ip = ip
                    fields_to_update.append("remote_ip")
                
                # Update the visitor object fields
                visitor.last_visit = now
                visitor.is_online = True
                
                # Save changes, using update_fields for efficiency
                visitor.save(update_fields=fields_to_update)

        response = self.get_response(request)
        return response