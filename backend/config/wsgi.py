import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# This is the standard Django variable
application = get_wsgi_application()

# --- ADD THIS LINE FOR VERCEL ---
app = application