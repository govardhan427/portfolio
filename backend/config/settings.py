import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# 1. CORE SECURITY SETTINGS (LOCAL DEV MODE)
# ==============================================================================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')
DEBUG = os.getenv('DEBUG') == 'True'
# WhiteNoise handles static files on production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', os.getenv('RENDER_EXTERNAL_HOSTNAME')]

# 2. Enforce HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Only allow connections from Render/your domain
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# ==============================================================================
# 2. INSTALLED APPS
# ==============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'rest_framework',          # The API Engine
    'corsheaders',             # Allows React to talk to Django
    'cloudinary_storage',      # (Prepared for Production)
    'cloudinary',              # (Prepared for Production)

    # Masterpiece Custom Apps
    'core',                    # Projects, Profile, Skills
    'analytics',               # The "Spy" Visitor Tracking
    'vault',                   # File Storage
    'blog',                    # CMS
    'features',                # AI, Steganography, etc.
]

# ==============================================================================
# 3. MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware', # MUST be at the top
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # For serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Custom "Spy" Middleware (We will uncomment this when we write the file)
    'analytics.middleware.VisitorTrackingMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ==============================================================================
# 4. DATABASE (SQLite for Local, Postgres for Prod)
# ==============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

# ==============================================================================
# 5. PASSWORD VALIDATION
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==============================================================================
# 6. INTERNATIONALIZATION
# ==============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# 7. STATIC & MEDIA FILES (Local Setup)
# ==============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media (Uploaded User Files)
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# CACHING CONFIGURATION (Add this block)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_data'), # Directory to store cache files
        'TIMEOUT': 300,  # Cache timeout in seconds (5 minutes)
        'OPTIONS': {
            'MAX_ENTRIES': 1000 # Max number of cache entries
        }
    }
}

# The cache key prefix helps isolate your project's cache data
CACHE_MIDDLEWARE_KEY_PREFIX = 'portfolio_cache'

# We'll apply caching to the Home View specifically, which is most beneficial.
# Cache will last 5 minutes (300 seconds)
HOME_CACHE_TIMEOUT = 300

# ==============================================================================
# 8. REST FRAMEWORK CONFIG
# ==============================================================================
REST_FRAMEWORK = {
    # Use JSON by default
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # For now, allow anyone to read. We lock it down later.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', 
    ],
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1), # Long time for dev
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
# ==============================================================================
# 9. CORS CONFIGURATION (Crucial for React)
# ==============================================================================
# For local dev, we allow all origins. 
# In production, we will restrict this to 'https://your-vercel-app.vercel.app'
CORS_ALLOW_ALL_ORIGINS = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ==============================================================================
# 10. CLOUDINARY CONFIGURATION (The Vault Storage)
# ==============================================================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "dqw1t0dul",
    'API_KEY': "467449637461852",
    'API_SECRET': "nd2vS0yVdxIuRZpuIHH0O0n8Q1E"
}

# Tell Django to use Cloudinary for uploaded media (files/images)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'