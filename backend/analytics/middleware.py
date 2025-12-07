# backend/analytics/middleware.py

from django.utils import timezone
from datetime import timedelta
from .models import Visitor

ACTIVE_WINDOW_MINUTES = 5       # How long a user stays “online” after activity
MIN_UPDATE_INTERVAL = 30        # Only update DB every 30 sec (prevents spam)

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

        # 2. Find or Create Visitor
        visitor, created = Visitor.objects.get_or_create(
            # Find by the session key
            session_key=session_key,
            defaults={
                # Use the corrected field names from models.py
                "remote_ip": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "visits": 1, 
                "last_visit": now,
                "is_online": True
            }
        )
        
        # 3. Handle Updates for Existing Visitor
        if not created:
            # Check for minimum update interval for performance
            if visitor.last_visit < now - timedelta(seconds=MIN_UPDATE_INTERVAL):
                
                # List fields we are going to update
                fields_to_update = ["last_visit", "is_online"]

                # New day check: increment visits
                if visitor.last_visit.date() < now.date():
                    visitor.visits += 1
                    fields_to_update.append("visits")

                # Update the visitor object fields
                visitor.last_visit = now
                visitor.is_online = True
                
                # Save changes, using update_fields for efficiency
                # Note: 'visits' is included conditionally, but safe to include if unchanged.
                visitor.save(update_fields=fields_to_update)

        response = self.get_response(request)
        return response