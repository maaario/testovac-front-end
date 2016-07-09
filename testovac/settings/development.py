from __future__ import absolute_import

from testovac.settings.common import *

DEBUG = True

SECRET_KEY = '-(tu4#dd!-9x9fmxvsq*psm^1+e+=r@ofes&6tk*e-gpk5mhn9'

SENDFILE_BACKEND = 'sendfile.backends.development'

THUMBNAIL_DEBUG = True

# Debug toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INSTALLED_APPS += (
    'debug_toolbar',
)
MIDDLEWARE_CLASSES = (
    ('debug_toolbar.middleware.DebugToolbarMiddleware',) +
    MIDDLEWARE_CLASSES
)
INTERNAL_IPS = ('127.0.0.1',)
