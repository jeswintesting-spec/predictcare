from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'bmh-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

# Added Django admin and authentication apps
INSTALLED_APPS = [
    'django.contrib.admin',          # <-- admin site
    'django.contrib.auth',           # authentication framework
    'django.contrib.contenttypes',
    'django.contrib.sessions',       # session support (required by admin)
    'django.contrib.messages',       # messaging framework (required by admin)
    'django.contrib.staticfiles',
    'hospital',
    'pharmacy',
    'accounts',
]

# Added essential middleware for sessions, auth, messages
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bmh_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'hospital.context_processors.hospital_roles',
            ],
        },
    },
]

WSGI_APPLICATION = 'bmh_project.wsgi.application'

# PostgreSQL Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bmh_hospital',
        'USER': 'bmh_admin',
        'PASSWORD': 'bmh_secure_2026',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# CSRF Settings for Development
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'hub'
LOGOUT_REDIRECT_URL = 'login'

import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
