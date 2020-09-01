from __future__ import unicode_literals
import os
import dj_database_url

# import our default settings
from casepro.settings_common import * # noqa

import environ

env = environ.Env(DEBUG=(bool, False))
# reading .env file
environ.Env.read_env()

DEBUG = False
SECRET_KEY = env.str("SECRET_KEY", default='REPLACEME')
TEMPLATE_DEBUG = DEBUG
COMPRESS_OFFLINE = True
SEND_EMAILS = True

HOSTNAME = env.str('HOSTNAME', default='localhost:8000')
SITE_HOST_PATTERN = env.str('SITE_HOST_PATTERN', default='http://%s.localhost:8000')

SITE_API_HOST = env.str('SITE_API_HOST', default='http://localhost:8001/')

SENTRY_DSN = env.str("SENTRY_DSN", default="")

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(
            'CASEPRO_DATABASE',
            'postgres://casepro:nyaruka@localhost/casepro')),
}

# SMTP Settings
EMAIL_HOST = env.str('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=25)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')

SITE_BACKEND = os.environ.get('SITE_BACKEND', 'casepro.backend.NoopBackend')
SITE_EXTERNAL_CONTACT_URL = os.environ.get('SITE_EXTERNAL_CONTACT_URL', 'http://localhost:8001/contact/read/%s/')

# Time until a case is re-assigned (specified in minutes)
SITE_CASE_RESPONSE_REQUIRED_TIME = env.int(
    'SITE_CASE_RESPONSE_REQUIRED_TIME', default=60)

SITE_HIDE_CONTACT_FIELDS = ["name"]
SITE_CONTACT_DISPLAY = env.str('SITE_CONTACT_DISPLAY',
                               default='name')
SITE_MAX_MESSAGE_CHARS = env.int('SITE_MAX_MESSAGE_CHARS', default=640)
# the max value for this is 800

REDIS_HOST = env.str('REDIS_HOST', default='localhost:6379')
REDIS_PORT = env.int('REDIS_PORT', default=15)

BROKER_URL = 'redis://%s/%d' % (REDIS_HOST, REDIS_PORT)  # noqa TESTING defined in settings_common (flake8)
CELERY_RESULT_BACKEND = BROKER_URL
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s/%d' % (REDIS_HOST, REDIS_PORT),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

USE_DEFAULT_CACHE = env.bool('USE_DEFAULT_CACHE', default=False)
if USE_DEFAULT_CACHE:
    # Use Django's default cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# settings_common currently defines Nyaruka contact details. We use sentry.
ADMINS = []

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['*'])

if SENTRY_DSN:
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }
