from django.conf import settings as django_settings

SUBMIT_DEBUG = bool(getattr(django_settings, 'SUBMIT_DEBUG', 'True'))

SUBMIT_PATH = getattr(django_settings, 'SUBMIT_PATH', 'submit/')

VIEWABLE_EXTENSIONS = getattr(django_settings, 'VIEWABLE_EXTENSIONS', ['.txt', '.pdf'])

UPLOADED_FILENAME_MAXLENGTH = int(getattr(django_settings, 'UPLOADED_FILENAME_MAXLENGTH', 128))

SUBMIT_DESCRIPTION_ALLOWED_EXTENSIONS = getattr(django_settings, 'SUBMIT_DESCRIPTION_ALLOWED_EXTENSIONS',
                                                ['.pdf', '.txt', '.md', '.rtf', '.doc', '.docx', '.odt']
                                                )
