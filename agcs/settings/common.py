import json
import os
from pathlib import Path
from machina import (
    get_apps as get_machina_apps,
    MACHINA_MAIN_TEMPLATE_DIR,
    MACHINA_MAIN_STATIC_DIR
)

PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

BASE_DIR = PROJECT_PACKAGE.parent

DATA_DIR = Path(os.environ['DJANGOPROJECT_DATA_DIR']) if (
    'DJANGOPROJECT_DATA_DIR' in os.environ
) else BASE_DIR.parent

LOG_DIR = DATA_DIR.joinpath('log', 'django')

try:
    with DATA_DIR.joinpath('conf', 'secrets.json').open() as handle:
        SECRETS = json.load(handle)
except IOError: # pragma: no cover
    SECRETS = {
        'secret_key': 'a',
        'superfeedr_creds': ['any@email.com', 'some_string'],
    }

RECAPTCHA_PUBLIC_KEY  = SECRETS.get('recaptcha_pub', '')
RECAPTCHA_PRIVATE_KEY = SECRETS.get('recaptcha_pri', '')
GOOGLE_API_KEY        = SECRETS.get('gapi_key', '')
EMAIL_HOST_USER       = SECRETS.get('email_host_user', '')
EMAIL_HOST_PASSWORD   = SECRETS.get('email_host_pass', '')
SECRET_KEY            = str(SECRETS['secret_key'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'agcs_db',
        'USER': 'django',
        'HOST': SECRETS.get('db_host', ''),
        'PASSWORD': SECRETS.get('db_password', ''),
    },
}

ROOT_URLCONF = 'agcs.urls.www'

WSGI_APPLICATION = 'agcs.wsgi.application'

ADMINS = MANAGERS  = (
    ('Alpha Geek', 'root@alphageek.xyz'),
)

DEFAULT_REPLY_ADDR = '"Alpha Geek (contact)" <contact@alphageek.xyz>'
DEFAULT_FROM_EMAIL = '"Alpha Geek (no-reply)" <no-reply@alphageek.xyz>'
SERVER_EMAIL = '"Alpha Geeks (root)" <root@alphageek.xyz>'


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ADMIN_URL        = 'admin/'
STATIC_URL       = '/s/'
MEDIA_URL        = '/m/'
LANGUAGE_CODE    = 'en-us'
TIME_ZONE        = 'America/Chicago'
EMAIL_HOST       = SECRETS.get('email_host', 'smtp.gmail.com')
EMAIL_PORT       = SECRETS.get('email_port', '587')
USE_I18N         = False
USE_L10N         = False
USE_TZ           = True
EMAIL_USE_TLS    = True
CSRF_COOKIE_HTTPONLY = True
SITE_ID = 1

USE_ETAGS        = True

STATICFILES_DIRS = [
    str(PROJECT_PACKAGE.joinpath('static')),
    MACHINA_MAIN_STATIC_DIR,
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'django_hosts',
    'landing.apps.LandingConfig',
    'snowpenguin.django.recaptcha2',
    'favicon',
    'bootstrap3',
    'django_assets',
    'mptt',
    'haystack',
    'whoosh',
    'widget_tweaks',
    'pagedown',
    'pytz',
    'community',
    'contact.apps.ContactConfig',
    'metadata.apps.MetadataConfig',
    'headers.apps.HeadersConfig',
    'myip.apps.MyIPConfig',
    'treenav',
    'pubdocs.apps.PubdocsConfig',
] + get_machina_apps([
    'community.apps.forum_conversation',
    'community.apps.forum_member',
])


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'headers.middleware.VaryAcceptEncodingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'community.middleware.BetterForumPermissionMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'headers.middleware.ViaHeaderMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(PROJECT_PACKAGE.joinpath('templates')),
            str(PROJECT_PACKAGE.joinpath('templates', 'community')),
            MACHINA_MAIN_TEMPLATE_DIR,
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'machina.core.context_processors.metadata',
                'landing.core.context_processors.extra',
                'landing.core.context_processors.services',
                'metadata.core.context_processors.links',
                'metadata.core.context_processors.website',
                'treenav.context_processors.treenav_active',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'full': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
         'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'class': 'logging.FileHandler',
            'formatter': 'full',
            'filename': str(LOG_DIR.joinpath(os.environ.get(
                'DJANGO_LOG_LEVEL', 'INFO').lower())) + '.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}

# django-hosts settings

DEFAULT_HOST = 'www'

HOST_SCHEME = 'http'

HOST_SITE_TIMEOUT = 3600

ROOT_HOSTCONF = 'agcs.hosts'

# django-machina settings

MIGRATION_MODULES = {
    'forum_conversation': 'machina.apps.forum_conversation.migrations',
    'forum_member': 'machina.apps.forum_member.migrations',
}

HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
    'PATH': str(DATA_DIR.joinpath('idx', 'whoosh_index')),
  },
}

MACHINA_FORUM_NAME = 'Alpha Geeks Forum'

MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
    'can_see_forum',
    'can_read_forum',
    'can_start_new_topics',
    'can_edit_own_posts',
    'can_post_without_approval',
    'can_create_polls',
    'can_vote_in_polls',
    'can_download_file',
]

COMPRESS_CSS_FILTERS=[
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSCompressorFilter',
]

COMPRESS_JS_FILTERS=[
    'compressor.filters.jsmin.JSMinFilter',
    'compressor.filters.jsmin.SlimItFilter',
]

FAVICON_PREFIX = 'img/favicon/'

DEFAULT_WEBSITE_NAME='www.alphageek.xyz'

LANGUAGES = [('en', 'English'),]
