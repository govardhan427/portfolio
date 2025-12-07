# backend/blog/models.py
from django.db import models
from django.utils.text import slugify

# Helper function to generate the correct URL
def generate_cloudinary_url(instance, filename):
    # This function is not used for the fix itself, but shows the goal.
    return f'blog/{filename}'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(help_text="Markdown Content")
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    
    # ... metadata fields ...

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # --- CRITICAL FIX: Override the file URL generation for the API ---
    # This fixes the display/API output if the path saved to the database is incomplete.
    @property
    def cover_image_url(self):
        if not self.cover_image:
            return None
        
        # Check if the URL already starts with the absolute path
        if str(self.cover_image.url).startswith('http'):
            return self.cover_image.url
        
        # Manually construct the full, correct Cloudinary URL structure
        # NOTE: You MUST replace 'dqw1t0dul' with the environment variable or hardcoded cloud name if needed
        CLOUD_NAME = 'dqw1t0dul'
        
        # This structure includes the resource type, version number, and file path
        # It relies on the database having saved the file name correctly (e.g., 'blog/miles-morales...')
        return f'https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{self.cover_image}'

    def __str__(self):
        return self.title