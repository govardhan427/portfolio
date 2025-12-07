from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # --- Custom Method for Cloudinary Image Display ---
    def image_tag(self, obj):
        """Generates a clickable link to the Cloudinary image URL."""
        if obj.cover_image:
            # mark_safe prevents Django from escaping the HTML <a> tag
            return mark_safe(f'<a href="{obj.cover_image.url}" target="_blank">View on Cloudinary</a>')
        return "No Image"
    image_tag.short_description = 'Cover Image Link' # Custom column header

    # What columns to show in the list
    # FIX: Add image_tag to list_display
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
            # FIX: Replace 'cover_image' with the custom 'image_tag'
            'fields': ('title', 'slug', 'cover_image', 'image_tag') 
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_published', 'read_time')
        }),
    )
    
    # CRITICAL: Tells the admin panel not to try and edit the tag method
    readonly_fields = ('image_tag',)