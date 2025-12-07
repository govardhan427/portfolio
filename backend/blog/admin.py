# backend/blog/admin.py

from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # --- Custom Method for Cloudinary Image Display (Used in fieldsets) ---
    def image_tag(self, obj):
        if obj.cover_image:
            return mark_safe(f'<a href="{obj.cover_image.url}" target="_blank">View on Cloudinary</a>')
        return "No Image"
    image_tag.short_description = 'Image Link'

    # --- FIX: Only use fields guaranteed to exist to avoid SystemCheckError ---
    # After migration runs successfully, we can put the full list back.
    list_display = ('title', 'is_published', 'created_at', 'read_time', 'image_tag')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'cover_image', 'image_tag') 
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
        # --- FIX: Temporarily remove all fields that don't exist yet ---
        ('Publishing', {
            'fields': [] 
        }),
    )
    
    readonly_fields = ('image_tag',)