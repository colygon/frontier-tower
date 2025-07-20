from .settings import *
import os

# Production settings for Vercel deployment
DEBUG = config('DEBUG', default=False, cast=bool)

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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For Vercel, we'll serve static files differently
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Security settings for production (disabled for initial deployment)
SECURE_SSL_REDIRECT = False  # Let Vercel handle SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = False  # Disable for initial testing
CSRF_COOKIE_SECURE = False  # Disable for initial testing

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://*.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for initial deployment
