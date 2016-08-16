# Django settings for testovac project.

import os

from django.contrib.messages import constants as message_constants
from django.http import UnreadablePostError

import testovac

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(
    os.path.dirname(os.path.realpath(testovac.__file__))
)


def env(name, default):
    return os.environ.get(name, default)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

ALLOWED_HOSTS = []

SITE_ID = 1

# HACK: competition and site should be connected
CURRENT_COMPETITION_PK = 'letna-skola'

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
    'sortedm2m',
    'testovac',
    'testovac.login',
    'testovac.menu',
    'testovac.submit',
    'testovac.tasks',
    'testovac.results',

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
    os.path.join(PROJECT_DIR, PROJECT_MODULE_NAME, 'locale'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = env('TESTOVAC_FRONT_MEDIA_ROOT', os.path.join(PROJECT_DIR, 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = env('TESTOVAC_FRONT_MEDIA_URL', '/media/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = env('TESTOVAC_FRONT_STATIC_URL', '/static/')

STATIC_ROOT = env('TESTOVAC_FRONT_STATIC_ROOT', os.path.join(PROJECT_DIR, PROJECT_MODULE_NAME, 'static'))

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
WIKI_ATTACHMENTS_EXTENSIONS = ['pdf', 'doc', 'odt', 'docx', 'txt', 'jpg', 'png', 'gif', 'zip']
WIKI_MARKDOWN_KWARGS = {
    'safe_mode': False,
    'output_format': 'html5',
}

# Task statements
TASKS_DEFAULT_SUBMIT_RECEIVER_TEMPLATE = 'source'
TASK_STATEMENTS_BACKEND = 'testovac.tasks.statements_backends.StatementsPDFBackend'
TASK_STATEMENTS_PATH = env('TESTOVAC_FRONT_TASK_STATEMENTS_PATH', os.path.join(PROJECT_DIR, 'statements'))


# Submit app
SUBMIT_POST_SUBMIT_FORM_VIEW = 'testovac.submit_configuration.PostSubmitFormCustomized'
SUBMIT_DISPLAY_SUBMIT_RECEIVER_NAME = 'testovac.submit_configuration.display_submit_receiver_name'
SUBMIT_DISPLAY_SCORE = 'testovac.submit_configuration.display_score'
JUDGE_DEFAULT_INPUTS_FOLDER_FOR_RECEIVER = 'testovac.submit_configuration.default_inputs_folder_at_judge'
SUBMIT_CAN_POST_SUBMIT = 'testovac.submit_configuration.can_post_submit'

SUBMIT_PATH = env('TESTOVAC_FRONT_SUBMIT_PATH', os.path.join(PROJECT_DIR, 'submit'))
JUDGE_INTERFACE_IDENTITY = env('TESTOVAC_FRONT_JUDGE_INTERFACE_IDENTITY', 'TESTOVAC')
JUDGE_ADDRESS = env('TESTOVAC_FRONT_JUDGE_ADDRESS', '127.0.0.1')
JUDGE_PORT = int(env('TESTOVAC_FRONT_JUDGE_PORT', 12347))


# Email for logging

if 'TESTOVAC_FRONT_ADMINS' in os.environ:
    ADMINS = tuple([tuple(admin.split(':')) for admin in env('TESTOVAC_FRONT_ADMINS', '').split(';')])
else:
    ADMINS = ()

if 'TESTOVAC_FRONT_MANAGERS' in os.environ:
    MANAGERS = tuple([tuple(manager.split(':')) for manager in env('TESTOVAC_FRONT_MANAGERS', '').split(';')])
else:
    MANAGERS = ()


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
def skip_unreadable_post(record):
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        if isinstance(exc_value, UnreadablePostError):
            return False
    return True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'skip_unreadable_posts': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_unreadable_post,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_unreadable_posts'],
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
