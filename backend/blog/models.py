from django.db import models
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(help_text="Markdown Content")
    cover_image = models.ImageField(upload_to='blog_files/', blank=True, null=True)
    # Metadata
    tags = models.CharField(max_length=200, help_text="Comma separated (e.g. Python, DevOps)")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_time = models.IntegerField(default=5, help_text="Estimated minutes")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title