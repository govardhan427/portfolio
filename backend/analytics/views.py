from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate 
from .models import Visitor, PageView
from .serializers import VisitorSerializer

# CRITICAL FIX: Imported get_ip_location to actually fetch the geographical data
from .utils import get_client_ip, get_ip_location
from rest_framework.permissions import AllowAny, IsAdminUser

# Define the active window (5 minutes) for a user to be considered "online"
ACTIVE_WINDOW_MINUTES = 5 
MIN_UPDATE_INTERVAL = 20 # Seconds to wait before updating visitor record again

# ==============================================================================
# 1. PUBLIC TRACKING ENDPOINT (Handles Visitor Activity and PageView logging)
# ==============================================================================
class TrackPageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Setup Session and Time
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        ip = get_client_ip(request)
        now = timezone.now()
        user_agent_raw = request.data.get("user_agent", "")

        # 2. Check if visitor already exists
        visitor = Visitor.objects.filter(session_key=session_key).first()
        created = False

        # 3. CRITICAL FIX: Create new visitor with parsed Location and Device data
        if not visitor:
            # Parse Device Type from User Agent
            ua_string = user_agent_raw.lower()
            if "mobi" in ua_string or "android" in ua_string or "iphone" in ua_string:
                device = "Mobile"
            elif "tablet" in ua_string or "ipad" in ua_string:
                device = "Tablet"
            else:
                device = "Desktop"

            # Fetch Geographical Location
            location_data = get_ip_location(ip)

            # Create the record
            visitor = Visitor.objects.create(
                session_key=session_key,
                remote_ip=ip,
                user_agent=user_agent_raw,
                device_type=device,          # Saves Mobile/Tablet/Desktop
                location=location_data,      # Saves actual geo-data from utils
                is_online=True,
                last_visit=now,
                visits=1                     # Initial visit count
            )
            created = True

        # 4. Rate Limiting Check (Skip expensive update if too soon)
        if not created and visitor.last_visit > now - timedelta(seconds=MIN_UPDATE_INTERVAL):
            # Log the page view but skip saving the Visitor record to the database
            path = request.data.get("path", "/")
            PageView.objects.create(
                visitor=visitor,
                path=path,
                referrer=request.data.get("referrer", "")
            )
            return Response({"status": "rate_limited"}, status=200)

        # 5. Handle Updates for Existing Visitor
        if not created:
            update_fields = ["last_visit", "is_online"]
            
            # New day check: Increment visits
            if visitor.last_visit.date() < now.date():
                visitor.visits += 1  
                update_fields.append("visits")
                
            # Update last visit time and set online status
            visitor.last_visit = now
            visitor.is_online = True
            
            # Update user agent if provided and changed
            if user_agent_raw and user_agent_raw != visitor.user_agent:
                visitor.user_agent = user_agent_raw
                update_fields.append("user_agent")
            
            # CRITICAL INTEGRITY FIX: Update remote_ip if it changed during the session
            if ip and visitor.remote_ip != ip:
                visitor.remote_ip = ip
                update_fields.append("remote_ip")
                # Optional: If the IP drastically changes, you could re-trigger get_ip_location here
            
            # Save changes to the Visitor record
            visitor.save(update_fields=update_fields)

        # 6. Log page view 
        PageView.objects.create(
            visitor=visitor,
            path=request.data.get("path", "/"),
            referrer=request.data.get("referrer", "")
        )

        return Response({"status": "tracked"}, status=status.HTTP_201_CREATED)

# ==============================================================================
# 2. ADMIN DASHBOARD API (Protected)
# ==============================================================================
class AnalyticsDashboardView(APIView):
    permission_classes = [IsAdminUser] 

    def get(self, request):
        now = timezone.now()
        
        # 1. EXPIRE STALE SESSIONS 
        timeout_time = now - timedelta(minutes=ACTIVE_WINDOW_MINUTES)
        
        # Set all records whose last activity was outside the window to offline
        Visitor.objects.filter(last_visit__lt=timeout_time, is_online=True).update(is_online=False)

        # 2. High-level Stats
        total_visitors = Visitor.objects.count()
        online_count = Visitor.objects.filter(is_online=True).count() 
        
        last_24h = now - timedelta(hours=24)
        active_today = Visitor.objects.filter(last_visit__gte=last_24h).count()
        total_pageviews = PageView.objects.count()

        # 3. Visitors Graph (Using TruncDate for PostgreSQL compatibility)
        last_7d = now - timedelta(days=7)
        daily_stats = (
            PageView.objects
            .filter(timestamp__gte=last_7d)
            .annotate(day=TruncDate("timestamp")) 
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # 4. Top Pages
        top_pages = (
            PageView.objects
            .values("path")
            .annotate(views=Count("id"))
            .order_by("-views")[:5]
        )

        return Response({
            'overview': {
                'total_visitors': total_visitors,
                'online_users': online_count,
                'active_today': active_today,
                'total_pageviews': total_pageviews,
            },
            'daily_stats': list(daily_stats),
            'top_pages': list(top_pages),
        })

class VisitorListView(viewsets.ReadOnlyModelViewSet):
    """
    Provides a list of all visitor records for the admin dashboard.
    """
    queryset = Visitor.objects.all().order_by('-last_visit')
    serializer_class = VisitorSerializer
    permission_classes = [permissions.IsAdminUser]