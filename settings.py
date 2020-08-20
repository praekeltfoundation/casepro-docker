from __future__ import unicode_literals
import os
import dj_database_url

# import our default settings
from casepro.settings_common import * # noqa

SECRET_KEY = os.environ.get('SECRET_KEY', 'REPLACEME')
if os.environ.get('DEBUG', 'False') == 'True':  # envvars are strings
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG
COMPRESS_OFFLINE = True
SEND_EMAILS = True

HOSTNAME = os.environ.get('HOSTNAME', 'localhost:8000')
SITE_HOST_PATTERN = os.environ.get('SITE_HOST_PATTERN', 'http://%s.localhost:8000')

SITE_API_HOST = os.environ.get('SITE_API_HOST', 'http://localhost:8001/')

SENTRY_DSN = os.environ.get('SENTRY_DSN')

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(
            'CASEPRO_DATABASE',
            'postgres://casepro:nyaruka@localhost/casepro')),
}

# SMTP Settings
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 25))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Time until a case is re-assigned (specified in minutes)
case_response_required_time_str = os.environ.get(
    'SITE_CASE_RESPONSE_REQUIRED_TIME')

if case_response_required_time_str:
    SITE_CASE_RESPONSE_REQUIRED_TIME = int(case_response_required_time_str)

SITE_HIDE_CONTACT_FIELDS = ["name"]
SITE_CONTACT_DISPLAY = os.environ.get('SITE_CONTACT_DISPLAY',
                                      'name')
SITE_MAX_MESSAGE_CHARS = 640  # the max value for this is 800

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost:6379')

BROKER_URL = 'redis://%s/%d' % (REDIS_HOST, 10 if TESTING else 15)  # noqa TESTING defined in settings_common (flake8)
CELERY_RESULT_BACKEND = BROKER_URL
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '%s:15' % REDIS_HOST,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

if os.environ.get('USE_DEFAULT_CACHE', 'False') == 'True':
    # Use Django's default cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# settings_common currently defines Nyaruka contact details. We use sentry.
ADMINS = []


ALLOWED_HOSTS = ['*']

if SENTRY_DSN:
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }
