# Django settings for testovac project.

import os
from django.contrib.messages import constants as message_constants

import testovac

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(
    os.path.dirname(os.path.realpath(testovac.__file__))
)


def env(name, default):
    return os.environ.get(name, default)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-(tu4#dd!-9x9fmxvsq*psm^1+e+=r@ofes&6tk*e-gpk5mhn9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Sites only needed for wiki
SITE_ID = 1

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'easy_select2',
    'taggit',
    'bootstrapform',
    'testovac',
    'testovac.login',
    'testovac.menu',
    'testovac.submit',
    'testovac.tasks',

    # wiki dependencies
    'django.contrib.sites',
    'django_nyt',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',

    'news',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'testovac.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

WSGI_APPLICATION = 'testovac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('TESTOVAC_FRONT_DATABASE_NAME', 'testovacfront'),
        'USER': env('TESTOVAC_FRONT_DATABASE_USER', 'testovacfront'),
        'PASSWORD': env('TESTOVAC_FRONT_DATABASE_PASSWORD', ''),
    },
}


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = env('TESTOVAC_FRONT_LANGUAGE_CODE', 'sk-SK')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = env('TESTOVAC_FRONT_TIME_ZONE', 'Europe/Bratislava')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = env('TESTOVAC_FRONT_MEDIA_ROOT', os.path.join(PROJECT_DIR, 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = env('TESTOVAC_FRONT_MEDIA_URL', '/media/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

AUTH_USER_MODEL = 'auth.User'

MESSAGE_TAGS = {
    message_constants.DEBUG: 'alert-debug',
    message_constants.INFO: 'alert-info',
    message_constants.SUCCESS: 'alert-success',
    message_constants.WARNING: 'alert-warning',
    message_constants.ERROR: 'alert-danger',
}

# Wiki settings
USE_SENDFILE = True
WIKI_ATTACHMENTS_PATH = env(
    'TESTOVAC_WIKI_ATTACHMENTS_PATH',
    os.path.join(MEDIA_ROOT, 'wiki_attachments/%aid/')
)
WIKI_ATTACHMENTS_EXTENSIONS = ['pdf', 'doc', 'odt', 'docx', 'txt', 'jpg', 'png', 'gif']
WIKI_MARKDOWN_KWARGS = {
    'safe_mode': False,
    'output_format': 'html5',
}
