from .common import *

ALLOWED_HOSTS = list(set([
    'alphageek.xyz',
    'www.alphageek.xyz',
    'community.alphageek.xyz',
    'myip.alphageek.xyz',
] + SECRETS.get('allowed_hosts', [])))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': SECRETS.get('memcached_host', '127.0.0.1:11211'),
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': str(DATA_DIR.joinpath('tmp')),
   }
}

#HOST_SCHEME = 'https'

#PARENT_HOST = 'alphageek.xyz'

DEBUG = True
#DEBUG = False

THUMBNAIL_DEBUG = DEBUG

CSRF_COOKIE_DOMAIN = None
#CSRF_COOKIE_DOMAIN = '.pool.alphageek.xyz'
#CSRF_COOKIE_DOMAIN = '.alphageek.xyz'

CSRF_COOKIE_SECURE = False
#CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = False
#SESSION_COOKIE_SECURE = True

#CSRF_COOKIE_HTTPONLY = True

#SESSION_COOKIE_HTTPONLY = True

#USE_X_FORWARDED_HOST = True

HTML_MINIFY = False

STATIC_ROOT = '/static/files'

MEDIA_ROOT = '/static/media'

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'

SILENCED_SYSTEM_CHECKS = ['security.W008',]
