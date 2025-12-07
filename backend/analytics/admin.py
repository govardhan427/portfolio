from django.contrib import admin
from .models import Visitor, PageView

class PageViewInline(admin.TabularInline):
    model = PageView
    extra = 0
    readonly_fields = ('path', 'timestamp', 'method', 'status_code', 'referrer')
    can_delete = False

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    # CRITICAL FIX 1: Add is_online and session_key for visibility, and use remote_ip.
    list_display = (
        'remote_ip', 
        'session_key', 
        'is_online', 
        'device_type', 
        'first_visit', 
        'last_visit_formatted'
    )
    
    # CRITICAL FIX 2: Add session_key, remote_ip, and is_online to readonly_fields 
    # if you want to prevent accidental editing, or keep them visible.
    # I'll include the essential fields for a complete view:
    readonly_fields = (
        'id', 
        'session_key', 
        'remote_ip', 
        'is_online', 
        'user_agent', 
        'first_visit', 
        'last_visit'
    ) 
    
    # Add filtering and searching for better admin experience
    list_filter = ('is_online', 'device_type', 'first_visit')
    search_fields = ('remote_ip', 'user_agent', 'session_key')
    
    inlines = [PageViewInline]

    def last_visit_formatted(self, obj):
        return obj.last_visit.strftime("%d %b %Y %H:%M")
    last_visit_formatted.short_description = "Last Seen"

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('path', 'visitor', 'timestamp', 'status_code')
    list_filter = ('path', 'status_code', 'method')