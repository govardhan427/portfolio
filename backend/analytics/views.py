from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import Visitor, PageView
from .serializers import VisitorSerializer
from .utils import get_client_ip
from rest_framework.permissions import AllowAny, IsAdminUser

# ==============================================================================
# 1. PUBLIC TRACKING ENDPOINT (React calls this on route change)
# ==============================================================================
class TrackPageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Identify the Visitor (by IP)
        ip = get_client_ip(request)
        visitor, _ = Visitor.objects.get_or_create(ip_address=ip)
        
        # 2. Update their "Last Seen"
        visitor.last_visit = timezone.now()
        
        # 3. Update device info if missing
        if request.data.get('user_agent'):
            visitor.user_agent = request.data.get('user_agent')
        visitor.save()

        # 4. Log the specific page they are looking at
        path = request.data.get('path', '/')
        PageView.objects.create(
            visitor=visitor,
            path=path,
            referrer=request.data.get('referrer', '')
        )

        return Response({"status": "tracked"}, status=status.HTTP_201_CREATED)

# ==============================================================================
# 2. ADMIN DASHBOARD API (Protected)
# ==============================================================================
class AnalyticsDashboardView(APIView):
    # In production, change AllowAny to IsAdminUser
    permission_classes = [IsAdminUser] 

    def get(self, request):
        # Time ranges
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)

        # 1. High-level Stats
        total_visitors = Visitor.objects.count()
        active_today = Visitor.objects.filter(last_visit__gte=last_24h).count()
        total_pageviews = PageView.objects.count()

        # 2. Visitors Graph (Last 7 Days)
        # We group by date to show a trend line
        daily_stats = (
            PageView.objects
            .filter(timestamp__gte=last_7d)
            .extra(select={'day': "date(timestamp)"}) # SQLite syntax (works in dev)
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        # Note: For Postgres (Production), we might need TruncDate instead of .extra()

        # 3. Top Pages
        top_pages = (
            PageView.objects
            .values('path')
            .annotate(views=Count('id'))
            .order_by('-views')[:5]
        )

        return Response({
            'overview': {
                'total_visitors': total_visitors,
                'active_today': active_today,
                'total_pageviews': total_pageviews,
            },
            'daily_stats': list(daily_stats),
            'top_pages': list(top_pages)
        })

class VisitorListView(viewsets.ReadOnlyModelViewSet):
    """
    Detailed list of every person who visited.
    """
    queryset = Visitor.objects.all().order_by('-last_visit')
    serializer_class = VisitorSerializer
    permission_classes = [permissions.IsAdminUser] # Lock this down in prod!