"""
Note about this ``settings.py``:
    This file contains all the usual default django settings.
    However, to make this more extensible and to hide certain settings
    from the public in the github project. A file called ``environment.py``
    must be created at the root level of this project. With a series of needed
    settings. See below for details
    
List of needed settings:
    # current working directory so settings are relative
    CWD = '/home/timjdavey/apps'
    
    # make up some key - mash the keyboard
    SECRET_KEY = '123abc'
    
    # database settings
    DATABASE_ENGINE = ''    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = ''      # Or path to database file if using sqlite3.
    DATABASE_USER = ''      # Not used with sqlite3.
    DATABASE_PASSWORD = ''  # Not used with sqlite3.
    DATABASE_HOST = ''      # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''      # Set to empty string for default. Not used with sqlite3.
    
    # facebook api confs (simply the keys provided from the app)
    # you will not be able to login via facebook to test
    # if you want to do so, you will need to setup a new sandbox app
    # with domain as http://localhost:8000/
    FACEBOOK_API_KEY = 'x'
    FACEBOOK_SECRET_KEY = 'x'
    
    # Solr / Solango configs
    # see http://timjdavey.com/post/423973736/installing-solr-on-mac-osx
    SOLR_SERVER = 'localhost:8983'
    SOLR_ROOT = ''
    SOLR_SCHEMA_PATH = "".join([SOLR_ROOT, '/solr/conf/schema.xml'])
    SOLR_DATA_DIR = "".join([SOLR_ROOT,'/solr/data'])
    
"""
try:
    import environment
except:
    raise ImportError, "Please create environment.py file in your base directory - see settings.py for details"
else:
    from environment import CWD

# Django settings for secret project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/London'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/templates/static/' % CWD

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static'

# The default domain of the `Site`
# set to http://localhost:8000
BASE_DOMAIN = 'http://localhost:8000'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '%smedia/' % MEDIA_URL

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "utilz.context_processors.globals",
)


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'socialauth.auth_backends.OpenIdBackend',
    #'socialauth.auth_backends.TwitterBackend',
    'perm.backends.ClaimFacebookBackend',
)

# basic highlighting for solango
SEARCH_HL_PARAMS = [
    ("hl", "true"),  # basic highlighting
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # facebook middleware, checks auth and gets info
    'facebook.djangofb.FacebookMiddleware',
    # gives a user a permission_level (see `perm` module)
    'perm.middleware.PermissionUserMiddleware',  
    # makes ajax responses pretty
    'utilz.middleware.AjaxExceptionResponse',
#    'bakery.middleware.UrlCacheMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    "%s/templates/" % CWD,
)

# Solr configs. Please make sure SOLR_ROOT, SOLR_SERVER are defined in `environment.py`
from environment import SOLR_ROOT, SOLR_SERVER
SOLR_SCHEMA_PATH = '%s/conf/schema.xml' % SOLR_ROOT
SOLR_DATA_DIR = '%s/data' % SOLR_ROOT
SEARCH_UPDATE_URL = "http://%s/solr/update" % SOLR_SERVER
SEARCH_SELECT_URL = "http://%s/solr/select" % SOLR_SERVER
SEARCH_PING_URLS = ("http://%s/solr/admin/ping" % SOLR_SERVER,)

# The SPAM_THRESHOLD is the number of people reporting an abject as spam
# required to determine that it really _is_ spam.
SPAM_THRESHOLD = 5

# Cache controls
CACHE_BACKEND = 'dummy:///'
# CACHE_BACKEND = 'file://' + os.path.join(CWD, 'cache')'


GOOGLE_MAPS_API = 'ABQIAAAAvwXvkPULsCttPx92SuRYTRQjCj0UumZXFnS2V9VgMlEAmeHurhSR91h9akRd-XBQcqEUSeKCSqxmvw'

START_DATE = (2010,02,15)
# If using localhost set
# GOOGLE_MAPS_API = 'ABQIAAAAvwXvkPULsCttPx92SuRYTRQCULP4XOMyhPd8d_NrQQEO8sT8XBR1Sc1KHWEXc4tREvAEr_dJS_Mb3w'
# in environment.py

INSTALLED_APPS = (
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # dependancies
    'openid_consumer',
    'socialauth',
    'solango',
    'south',
    # internal
    'accounts',
    'comment',
    'communication',
    'city',
    'discussion',
    'perm',
    'photo',
    'secret',
    'utilz',
    
    #'bakery',
)

# see top of document for notes
from environment import *


