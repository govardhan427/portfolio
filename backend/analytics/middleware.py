from django.utils import timezone
from .models import Visitor, PageView
from .utils import get_client_ip, get_ip_location

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # Filter out static/admin
        if not (path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/')):
            
            ip = get_client_ip(request)
            visitor = Visitor.objects.filter(ip_address=ip).first()

            if not visitor:
                # New Visitor? Get Location immediately
                location_data = get_ip_location(ip)
                visitor = Visitor.objects.create(
                    ip_address=ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                    location=location_data
                )
            else:
                # Existing Visitor?
                # FIX: If location is missing/empty, fetch it now!
                if not visitor.location: 
                    visitor.location = get_ip_location(ip)
                
                visitor.last_visit = timezone.now()
                visitor.save()

            # Log Page View
            PageView.objects.create(
                visitor=visitor,
                path=path,
                method=request.method,
                referrer=request.META.get('HTTP_REFERER', '')[:500]
            )

        response = self.get_response(request)
        return response