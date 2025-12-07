from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage # <--- Import this

class PrivateFile(models.Model):
    # ... categories ...
    CATEGORY_CHOICES = [
        ('RESUME', 'Resume & CV'),
        ('DOCS', 'Personal Documents'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=100)
    
    # 🚨 FORCE CLOUDINARY HERE:
    file = models.FileField(
        upload_to='vault/', 
        storage=RawMediaCloudinaryStorage() # <--- This forces Cloudinary usage
    )
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=20, blank=True)

    # ... keep the rest of your methods (save, str) ...
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.file:
            try:
                self.size = f"{self.file.size / 1024:.2f} KB"
            except:
                self.size = "Unknown"
        super().save(*args, **kwargs)