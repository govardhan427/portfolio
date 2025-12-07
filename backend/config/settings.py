import os
import json 
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
# 1. CORE SECURITY SETTINGS
# ==============================================================================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')
DEBUG = os.getenv("DEBUG", "False") == "True" 
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', os.getenv('RENDER_EXTERNAL_HOSTNAME')]

# 2. Enforce HTTPS (ONLY active in production when DEBUG=False)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
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
    'rest_framework', 
    'corsheaders', 
    'cloudinary_storage', 
    'cloudinary', 

    # Masterpiece Custom Apps
    'core', 
    'analytics', 
    'vault', 
    'blog', 
    'features', 
]

# ==============================================================================
# 3. MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
DB_URL = os.getenv('DATABASE_URL')

if DB_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DB_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
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
# 7. STATIC & MEDIA FILES (THE FIX IS HERE)
# ==============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = 'https://res.cloudinary.com/dqw1t0dul/'


# ==============================================================================
# 8. CACHING CONFIGURATION
# ==============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_data'),
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = 'portfolio_cache'
HOME_CACHE_TIMEOUT = 300

# ==============================================================================
# 9. REST FRAMEWORK CONFIG
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', 
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ==============================================================================
# 10. CLOUDINARY CONFIGURATION
# ==============================================================================
CLOUDINARY = {
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
}

CLOUDINARY_STORAGE = {
    # Keep this section, but it mostly relies on the CLOUDINARY dictionary above
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}
# ==============================================================================
# 11. CORS CONFIGURATION (THE FIX)
# ==============================================================================
# Read the comma-separated string from the environment
CORS_ORIGINS_STRING = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173')

# Parse the string into a Python list
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in CORS_ORIGINS_STRING.split(',')
]

# Disable this for security, forcing it to respect the list above
CORS_ALLOW_ALL_ORIGINS = False 

# ==============================================================================
# 12. DEFAULT AUTO FIELD
# ==============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'