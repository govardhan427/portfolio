# backend/core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Project
from .og_generator import generate_project_og
import sys
import os
# Import io for the BytesIO object needed for the file buffer
import io 

@receiver(post_save, sender=Project)
def generate_og_image(sender, instance, created, update_fields=None, **kwargs):
    # --- CRITICAL FIX 1: Prevent Recursive Loop ---
    # If the signal was triggered by the save() operation *we* performed on 'og_image', RETURN.
    # This prevents the save(update_fields=['og_image']) call from triggering itself.
    if update_fields is not None and ('og_image' in update_fields or 'og_image' not in instance._meta.fields):
        return

    # Only run if the Project has the required data and is not being deleted
    if not instance.title or not instance.tagline or kwargs.get('raw'):
        return

    # Check if the image already exists (and is correctly named)
    og_filename = f'{instance.slug}_og.png'
    target_path = os.path.join('project_og', og_filename)

    # Check 2: Only proceed if the file field is currently empty OR the slug changed.
    if instance.og_image.name == target_path and not created:
         # File already exists at the expected path, no need to regenerate/re-upload unless logic requires it.
         return
         
    # 1. Generate the image buffer (io.BytesIO object)
    try:
        image_buffer = generate_project_og(instance.title, instance.tagline)
    except Exception as e:
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
    # We use save=False initially, then update_fields=['og_image'] to commit the change.
    instance.og_image.save(og_filename, django_file, save=False)
    
    # Save the instance again to commit the file path. This is safe due to FIX 1.
    try:
        # CRITICAL FIX 2: Use update_fields=['og_image'] to ensure this save does not trigger other signals
        # and most importantly, is caught by FIX 1, preventing recursion.
        instance.save(update_fields=['og_image'])
    except Exception as e:
        print(f"Error saving OG image field: {e}")