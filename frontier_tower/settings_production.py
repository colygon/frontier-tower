from .settings import *
import os

# Production settings for Vercel deployment
DEBUG = False

# Vercel automatically sets these
ALLOWED_HOSTS = ['*']  # Vercel handles the domain routing

# Database for production (using SQLite for simplicity, can be changed to PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',  # Vercel uses /tmp for writable files
    }
}

# Static files configuration for Vercel
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://*.vercel.app",
]

CORS_ALLOW_ALL_ORIGINS = False  # Set to True if needed for development
