# backend/core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Project
from .og_generator import generate_project_og
import sys
import os

@receiver(post_save, sender=Project)
def generate_og_image(sender, instance, created, **kwargs):
    # Only run if the Project has the required data and is not being deleted
    if not instance.title or not instance.tagline or kwargs.get('raw'):
        return

    # 1. Generate the image buffer (io.BytesIO object)
    image_buffer = generate_project_og(instance.title, instance.tagline)
    
    # 2. Convert the buffer to a Django File object
    og_filename = f'{instance.slug}_og.png'
    
    django_file = InMemoryUploadedFile(
        file=image_buffer,
        field_name=None,
        name=og_filename,
        content_type='image/png',
        size=sys.getsizeof(image_buffer),
        charset=None
    )

    # 3. CRITICAL: Prevent infinite loop when saving the file
    current_og_image_name = instance.og_image.name if instance.og_image else None
    target_path = os.path.join('project_og', og_filename) # Expected path in media storage
    
    # Check if a file already exists at the target path to avoid re-uploading the same file path
    # Django will automatically check if the path is identical.
    if current_og_image_name != target_path:
        
        # Save the generated file to the og_image field (saves to local media)
        instance.og_image.save(og_filename, django_file, save=False)
        
        # Save the instance again with save=True to commit the file path to the database.
        # Use update_fields to prevent the signal from running again immediately
        # due to the recursive save (if your Django version handles it this way).
        try:
            instance.save(update_fields=['og_image'])
        except Exception as e:
            # Handle potential race conditions or transactional errors gracefully
            print(f"Error saving OG image field: {e}")