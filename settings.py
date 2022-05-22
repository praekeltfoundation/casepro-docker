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
CSRF_TRUSTED_ORIGINS = [SITE_HOST_PATTERN % ("*")]

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
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)

DEFAULT_FROM_EMAIL= env.str('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

SITE_BACKEND = os.environ.get('SITE_BACKEND', 'casepro.backend.NoopBackend')
SITE_EXTERNAL_CONTACT_URL = os.environ.get('SITE_EXTERNAL_CONTACT_URL', 'http://localhost:8001/contact/read/%s/')

# Time until a case is re-assigned (specified in minutes)
SITE_CASE_RESPONSE_REQUIRED_TIME = env.int(
    'SITE_CASE_RESPONSE_REQUIRED_TIME', default=60)

SITE_HIDE_CONTACT_FIELDS = ["name"]
SITE_CONTACT_DISPLAY = env.str('SITE_CONTACT_DISPLAY',
                               default='name')
SITE_REDACT_URNS = env.bool('SITE_REDACT_URNS', default=True)
SITE_MAX_MESSAGE_CHARS = env.int('SITE_MAX_MESSAGE_CHARS', default=640)
# the max value for this is 800

REDIS_HOST = env.str('REDIS_HOST', default='localhost:6379')
REDIS_PORT = env.int('REDIS_PORT', default=15)

CELERY_BROKER_URL = 'redis://%s/%d' % (REDIS_HOST, REDIS_PORT)  # noqa TESTING defined in settings_common (flake8)
BROKER_URL = CELERY_BROKER_URL
broker_url = CELERY_BROKER_URL
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

# How often (in seconds) to sync messages with the backend
MESSAGE_SYNC_INTERVAl = env.int('MESSAGE_SYNC_INTERVAl', default=60)
# Overwrite message-pull schedule to use the above interval
CELERY_BEAT_SCHEDULE ["message-pull"]= {
    "task": "dash.orgs.tasks.trigger_org_task",
    "schedule": timedelta(seconds=MESSAGE_SYNC_INTERVAl),
    "args": ("casepro.msgs.tasks.pull_messages", "sync"),
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
