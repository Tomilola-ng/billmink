""" Django Settings """

import os
from pathlib import Path

import dj_database_url
import environ

env = environ.Env()
environ.Env.read_env()


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY')

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']


# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',

    # My apps
    'bills',
    'accounts',
    'campaigns',

    # Modules
    'hitcount',
    "phonenumber_field",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'Templates'],
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

# Database
DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL'))
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfile')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
    Custom Settings
"""

SITE_ID = 1
SITE_URL = "127.0.0.1:8000"
SITE_DOMAIN = "127.0.0.1:8000"

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'login_view'
LOGIN_REDIRECT_URL = 'index_view'
LOGOUT_REDIRECT_URL = 'index_view'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DOMAIN_PATH = 'http://127.0.0.1:8000'

"""
    Deployment Settings
"""

# Simplified static file serving.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
