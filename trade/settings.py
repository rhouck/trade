"""
Django settings for trade project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Use site-specific settings
from os import environ
host = environ.get('MODE', '')
from re import search

if search('live', host):
    from settings_live import *
    LIVE = True
elif search('dev', host):
    from settings_dev import *
    LIVE = False
else:
    from settings_local import *
    LIVE = False

# create sqlite3 db for testing purposes
import sys
if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY') 


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_rq",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'trade.urls'

WSGI_APPLICATION = 'trade.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# register parse
from parse_rest.connection import register
PARSE_CONFIG = {'app_id': environ.get('PARSE_APPLICATION_ID'), 'api_key': environ.get('PARSE_REST_API_KEY'), 'master_key': environ.get('PARSE_REST_API_KEY')}
register(PARSE_CONFIG['app_id'], PARSE_CONFIG['api_key'])


# setup redis queue
RQ_QUEUES = {
    
    'default': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # If you're on Heroku
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    },
    'high': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # If you're on Heroku
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # If you're on Heroku
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    }
}

try:
    import django_rq
    REDIS_CONN = django_rq.get_connection()
except:
    pass