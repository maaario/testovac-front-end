from django.conf import settings as django_settings

SUBMIT_PATH = getattr(django_settings, 'SUBMIT_PATH', 'submit/')

UPLOADED_FILENAME_MAXLENGTH = int(getattr(django_settings, 'UPLOADED_FILENAME_MAXLENGTH', 128))
