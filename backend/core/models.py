from django.db import models

# ==========================================
# 1. SKILLS (The Building Blocks)
# ==========================================
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('LANG', 'Languages (Python, JS)'),
        ('FRONT', 'Frontend (React, CSS)'),
        ('BACK', 'Backend (Django, Node)'),
        ('DEVOPS', 'DevOps (Docker, AWS)'),
        ('TOOL', 'Tools (Git, Linux)'),
    ]

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(default=0, help_text="0 to 100")
    icon_class = models.CharField(max_length=50, blank=True, help_text="FontAwesome class or similar")
    is_featured = models.BooleanField(default=False, help_text="Show on Home Page?")

    def __str__(self):
        return self.name

# ==========================================
# 2. PROJECTS (The Masterpieces)
# ==========================================
class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="URL friendly name (e.g. 'ecommerce-api')")
    tagline = models.CharField(max_length=200, help_text="Short one-liner description")
    description = models.TextField(help_text="Full details (Markdown supported)")
    
    # CRITICAL FIX 1: New field for the featured image URL
    featured_image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Paste the absolute URL for the main featured image.")
    # The "Flex" Relations
    skills = models.ManyToManyField(Skill, related_name='projects')
    
    # Links
    demo_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    
    # Metadata
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# ==========================================
# 3. PROJECT IMAGES (Carousel Support)
# ==========================================
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    
    # CRITICAL FIX 2: Replaced ImageField with URLField
    image_url = models.URLField(max_length=500, help_text="Paste the absolute URL for this gallery image.")
    
    caption = models.CharField(max_length=200, blank=True)
    is_feature = models.BooleanField(default=False, help_text="Is this the main cover image?")

    def __str__(self):
        return f"Image for {self.project.title}"

# ==========================================
# 4. CERTIFICATIONS (The Proof)
# ==========================================
class Certificate(models.Model):
    name = models.CharField(max_length=100)
    issuer = models.CharField(max_length=100)
    date_issued = models.DateField()
    credential_url = models.URLField(blank=True)
    
    # CRITICAL FIX 3: Replaced ImageField with URLField
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Paste the absolute URL for the certificate image.")

    def __str__(self):
        return self.name
        
# ... Journey and Achievement models are correct and unchanged ...

class Journey(models.Model):
    CATEGORY_CHOICES = [
        ('EDU', 'Education'),
        ('WORK', 'Work / Internship'),
        ('ACHIEVEMENT', 'Achievement'),
        ('GOAL', 'Future Goal'),
    ]

    title = models.CharField(max_length=100) 
    subtitle = models.CharField(max_length=100) 
    date_range = models.CharField(max_length=50) 
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='EDU')
    order = models.IntegerField(default=0, help_text="Lowest number appears first")
    
    class Meta:
        ordering = ['order'] 

    def __str__(self):
        return f"{self.date_range} - {self.title}"

class Achievement(models.Model):
    title = models.CharField(max_length=100) 
    description = models.TextField()
    date_earned = models.DateField()
    icon_name = models.CharField(max_length=50, default='Trophy', help_text="Icon name (Trophy, Star, Code, Zap, GitBranch)")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title