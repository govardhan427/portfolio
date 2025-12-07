from django.contrib import admin
from django.utils.safestring import mark_safe # Needed for showing the URL as a link
from .models import Skill, Project, ProjectImage, Certificate, Journey, Achievement

# --- Inline for Project Images (Gallery) ---
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    
    # CRITICAL FIX 1: Display the URL field instead of the file field
    fields = ('image_url', 'caption', 'is_feature')
    
    # Optional: If you want to see the image thumbnail or link, add a custom method
    def image_preview(self, obj):
        if obj.image_url:
            # Displays the URL as a clickable link
            return mark_safe(f'<a href="{obj.image_url}" target="_blank">View Image</a>')
        return "No URL"
    image_preview.short_description = 'Preview'
    
    # If using image_preview, you would add it to fields:
    # fields = ('image_url', 'image_preview', 'caption', 'is_feature')
    # readonly_fields = ('image_preview',)

# --- Admin for Project ---
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # CRITICAL FIX 2: Update fieldsets to use the new 'featured_image_url' field
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'tagline', 'featured_image_url', 'featured') # Updated field
        }),
        ('Details', {
            'fields': ('description', 'skills')
        }),
        ('Links', {
            'fields': ('demo_link', 'github_link')
        }),
    )

    list_display = ('title', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    filter_horizontal = ('skills',)

# --- Admin for Skill (No image fields, no change needed) ---
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'is_featured')
    list_filter = ('category', 'is_featured')

# --- Admin for Certificate ---
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    # CRITICAL FIX 3: Add the image_url field to the list display and fields
    list_display = ('name', 'issuer', 'date_issued')
    fieldsets = (
        (None, {
            'fields': ('name', 'issuer', 'date_issued', 'credential_url', 'image_url')
        }),
    )

# --- Admin for Journey & Achievement (No image fields, no change needed) ---
@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ('date_range', 'title', 'category', 'order')
    list_editable = ('order',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_earned', 'icon_name', 'order')
    list_editable = ('order', 'icon_name')