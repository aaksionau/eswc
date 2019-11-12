import os
from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

STATIC_ROOT = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
