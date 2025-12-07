# backend/core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Project
from .og_generator import generate_project_og
import sys
import os
import io 

@receiver(post_save, sender=Project)
def generate_og_image(sender, instance, created, update_fields=None, **kwargs):
    # --- CRITICAL FIX 1: Prevent Recursive Loop ---
    # If this signal was triggered by the instance.save(update_fields=['og_image']) call, exit immediately.
    # This prevents the signal from calling itself indefinitely.
    if update_fields and 'og_image' in update_fields:
        return

    # Check if the project has the required data (title/tagline) and is not a raw database load.
    if not instance.title or not instance.tagline or kwargs.get('raw'):
        return

    # Check 2: Only proceed if the file field is currently empty OR the slug changed 
    # (to avoid regenerating on every trivial save).
    og_filename = f'{instance.slug}_og.png'
    target_path = os.path.join('project_og', og_filename)
    
    # Check if a file already exists at the expected path AND the object wasn't just created.
    # We assume if the name matches and it's not a new object, the image is fine.
    if not created and instance.og_image.name == target_path:
         return
         
    # 1. Generate the image buffer (io.BytesIO object)
    try:
        image_buffer = generate_project_og(instance.title, instance.tagline)
    except Exception as e:
        # Catch exceptions related to PIL/font issues (common in cloud environments)
        print(f"Error generating OG image: {e}")
        return
    
    # 2. Convert the buffer to a Django File object
    django_file = InMemoryUploadedFile(
        file=image_buffer,
        field_name=None,
        name=og_filename,
        content_type='image/png',
        size=sys.getsizeof(image_buffer),
        charset=None
    )

    # 3. Save the generated file
    # Sets the path on the instance without hitting the database yet.
    instance.og_image.save(og_filename, django_file, save=False)
    
    # Save the instance again to commit the file path to the database.
    try:
        # CRITICAL FIX 2: update_fields=['og_image'] triggers the signal again, 
        # but FIX 1 catches and stops it.
        instance.save(update_fields=['og_image'])
    except Exception as e:
        print(f"Error saving OG image field: {e}")