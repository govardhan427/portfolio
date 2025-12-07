from django.contrib import admin
from .models import Visitor, PageView

class PageViewInline(admin.TabularInline):
    model = PageView
    extra = 0
    readonly_fields = ('path', 'timestamp', 'method', 'status_code', 'referrer')
    can_delete = False

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('remote_ip', 'device_type', 'first_visit', 'last_visit_formatted')
    readonly_fields = ('id', 'first_visit', 'last_visit') # Keep IP and Location editable for your manual test
    inlines = [PageViewInline]

    def last_visit_formatted(self, obj):
        return obj.last_visit.strftime("%d %b %Y %H:%M")
    last_visit_formatted.short_description = "Last Seen"

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('path', 'visitor', 'timestamp', 'status_code')
    list_filter = ('path', 'status_code', 'method')