from .common import *  # noqa

ALLOWED_HOSTS = list(set([
    'alphageek.dev',
    'www.alphageek.dev',
    'community.alphageek.dev',
    'myip.alphageek.dev',
    'staging.alphageek.xyz',
] + SECRETS.get('allowed_hosts', [])))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': SECRETS.get('memcached_host', '127.0.0.1:11211'),
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
   }
}

DEBUG = True

THUMBNAIL_DEBUG = DEBUG

CSRF_COOKIE_SECURE = False

CSRF_COOKIE_DOMAIN = None

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = '/static/media_root'

SESSION_COOKIE_SECURE = False

STATIC_ROOT = '/static/static_root'

if DEBUG:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        INSTALLED_APPS.append('debug_toolbar')
        INTERNAL_IPS = ['127.0.0.1']
        MIDDLEWARE.insert(
            MIDDLEWARE.index('django.middleware.common.CommonMiddleware') + 1,
            'debug_toolbar.middleware.DebugToolbarMiddleware')
    RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    HTML_MINIFY = False
