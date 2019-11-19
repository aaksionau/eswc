import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['eswc.paloni.webfactional.com',
                 'www.eastsidewrestling.org', 'eastsidewrestling.org']

STATIC_URL = "/static/"
STATIC_ROOT = '/home/paloni/webapps/eswc/eswc/all_static_files/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "all_static_files")
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True

EMAIL_HOST = config('SMTP_SERVER')
EMAIL_PORT = config('SMTP_PORT')
EMAIL_HOST_USER = config('MAIL_USER')
EMAIL_HOST_PASSWORD = config('MAIL_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
