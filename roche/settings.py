# coding=utf-8
#
# Django settings for roche project.
#

import os

from django.utils.translation import ugettext_lazy as _


PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '../')

#
# eXist-db
#
EXISTDB_SERVER_USER = 'admin'
EXISTDB_SERVER_PASSWORD = 'glen32'
EXISTDB_ROOT_COLLECTION = '/docker'
EXISTDB_SERVER_URL = 'http://{0}:{1}/exist'.format(
    os.environ['XMLDB_PORT_8080_TCP_ADDR'],
    os.environ['XMLDB_PORT_8080_TCP_PORT'])
EXISTDB_INDEX_CONFIGFILE = os.path.join(PROJECT_ROOT, 'roche', 'exist_index.xconf')

#
# fuseki
#
FUSEKI_QUERY_URL = 'http://{0}:{1}/ds/query'.format(
    os.environ['SPARQL_PORT_3030_TCP_ADDR'],
    os.environ['SPARQL_PORT_3030_TCP_PORT'])

FUSEKI_UPDATE_URL = 'http://{0}:{1}/ds/update'.format(
    os.environ['SPARQL_PORT_3030_TCP_ADDR'],
    os.environ['SPARQL_PORT_3030_TCP_PORT'])

#
# djiki
#
DJIKI_IMAGES_PATH = '/tmp'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('David Höppner', '0xffea@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docker',
        'USER': 'docker',
        'PASSWORD': os.environ['DOCKER_PASSWORD'],
        'HOST': os.environ['DB_PORT_5432_TCP_ADDR'],
        'PORT': os.environ['DB_PORT_5432_TCP_PORT'],
    }
}

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
    ('zh', _('Chinese (Mainland)')),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/tmp'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'static_root'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5kop1q!tkypa#t%18zoi2&(4ff+px-q@n@h08f-n=nq*(8yj(y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'roche.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'roche.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, os.path.join('dijiki', 'templates')),
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'djiki',
    'eulxml',
    'eulexistdb',
    'leaflet',
    'sparql',
    'ocr',
    'r',
    'annotate',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
