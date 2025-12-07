from django.contrib import admin
from .models import Skill, Project, ProjectImage, Certificate, Journey, Achievement

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline] # Allows adding images directly inside the Project screen
    filter_horizontal = ('skills',) # Nice UI for selecting multiple skills

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'is_featured')
    list_filter = ('category', 'is_featured')

admin.site.register(Certificate)
@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ('date_range', 'title', 'category', 'order')
    list_editable = ('order',) # Allows quick reordering in the list view
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_earned', 'icon_name', 'order')
    list_editable = ('order', 'icon_name')