from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # --- Custom Method for Cloudinary Image Display (The Fix) ---
    def image_tag(self, obj):
        """Generates a working link to the Cloudinary image URL."""
        if obj.cover_image:
            # obj.cover_image.url now returns the correct absolute URL 
            return mark_safe(f'<a href="{obj.cover_image.url}" target="_blank">View on Cloudinary</a>')
        return "No Image"
    image_tag.short_description = 'Image Link'

    # What columns to show in the list
    list_display = ('title', 'is_published', 'created_at', 'read_time', 'image_tag')
    
    # Sidebar filters
    list_filter = ('is_published', 'created_at')
    
    # Search bar capability
    search_fields = ('title', 'content', 'tags')
    
    # Magic: Auto-fill the slug field when you type the title
    prepopulated_fields = {'slug': ('title',)}
    
    # Layout adjustment for better writing experience
    fieldsets = (
        (None, {
            # Inject image_tag here for direct display next to the file field
            'fields': ('title', 'slug', 'cover_image', 'image_tag') 
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_published', 'read_time')
        }),
    )
    
    # CRITICAL: Mark image_tag as read-only
    readonly_fields = ('image_tag',)