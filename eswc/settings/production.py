import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['eswc.paloni.webfactional.com',
                 'www.eastsidewrestling.org', 'eastsidewrestling.org']

STATIC_URL = "/static/"
STATIC_ROOT = '/home/paloni/webapps/eswc/eswc/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
