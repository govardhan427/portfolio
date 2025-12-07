# backend/blog/admin.py

from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # REMOVE the image_tag method entirely (it's no longer needed)

    list_display = ('title', 'is_published', 'created_at', 'read_time')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            # CRITICAL CHANGE: Use the new URL field
            'fields': ('title', 'slug', 'cover_image_url')
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_published', 'read_time')
        }),
    )
    
    # CRITICAL CHANGE: Remove readonly_fields entirely, or ensure it's empty
    # readonly_fields = ('image_tag',) <-- DELETE THIS