from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # What columns to show in the list
    list_display = ('title', 'is_published', 'created_at', 'read_time')
    
    # Sidebar filters
    list_filter = ('is_published', 'created_at')
    
    # Search bar capability
    search_fields = ('title', 'content', 'tags')
    
    # Magic: Auto-fill the slug field when you type the title
    prepopulated_fields = {'slug': ('title',)}
    
    # Layout adjustment for better writing experience
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'cover_image')
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_published', 'read_time')
        }),
    )