from __future__ import absolute_import

from django.core.exceptions import ImproperlyConfigured

from testovac.settings.common import *

DEBUG = False
THUMBNAIL_DEBUG = False

SENDFILE_BACKEND = 'sendfile.backends.development'


def requiredenv(name):
    if name not in os.environ:
        raise ImproperlyConfigured("Value %s missing in environment configuration" % name)
    return os.environ.get(name)


SECRET_KEY = requiredenv('TESTOVAC_FRONT_SECRET_KEY')
ALLOWED_HOSTS = requiredenv('TESTOVAC_FRONT_ALLOWED_HOSTS').split(';')

# Dummy email configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
