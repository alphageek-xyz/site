import os
from agcs.settings.prod import *

SECRET_KEY = 'fake-key'
SECURE_SSL_REDIRECT = False
ALLOWED_HOSTS.append('testserver')
INSTALLED_APPS += ["tests",]
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
HTML_MINIFY = False

if locals().get('LOGGING'):
    del(LOGGING)

if os.environ.get('TRAVIS_CL_TEST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'agcs_db',
            'USER': 'postgres',
       },
   }
elif not locals().get('DATABASES'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'agcs_db',
         },
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
    }
}

STATIC_URL = '/s/'
STATIC_ROOT = '/tmp'
ROOT_URLCONF = 'tests.urls'

