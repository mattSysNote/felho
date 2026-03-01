"""
Django settings for photoupload project.
"""

from pathlib import Path
import os

# DIR:
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY (https://docs.djangoproject.com/en/6.0/topics/security/)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-dev-only')

allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
csrf_trusted_env = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost,http://127.0.0.1')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_trusted_env.split(',') if origin.strip()]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
if not DEBUG:
    SECURE_SSL_REDIRECT = True # only https

    SESSION_COOKIE_SECURE = True # only https for cookies

    CSRF_COOKIE_SECURE = True # only https for CSRF

    SECURE_HSTS_SECONDS = 31536000  # 1 év
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gallery',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csp.ContentSecurityPolicyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'photoupload.urls'

from django.utils.csp import CSP
SECURE_CSP = {
    "default-src": [CSP.SELF],
    "style-src": [
        "'self'",
        "https://fonts.googleapis.com",
        "https://cdnjs.cloudflare.com",
        "'unsafe-inline'" # tailwindcss static generation needed with npm
    ],
    "script-src": [
        "'self'",
        "https://cdn.tailwindcss.com",
        "'unsafe-eval'" # tailwindcss static generation needed with npm.
    ],
    "font-src": [
        "'self'",
        "https://fonts.gstatic.com",
        "https://cdnjs.cloudflare.com"
    ],
    "img-src": [
        "'self'",
        "data:",
        "https://cdnjs.cloudflare.com",
        "https://*.gstatic.com",
    ]
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'gallery' / 'templates'],
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

WSGI_APPLICATION = 'photoupload.wsgi.application'


# Database
if os.environ.get('DB_NAME') and os.environ.get('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    print("PostgreSQL setup is missing!")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
# This defines where collectstatic will put files in the container
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration for serving static files in production
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Login/Logout
LOGIN_REDIRECT_URL = 'photo_list'
LOGOUT_REDIRECT_URL = 'photo_list'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'