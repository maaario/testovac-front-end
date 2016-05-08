from django.conf import settings as django_settings
from django.contrib import messages

SUBMIT_PATH = getattr(django_settings, 'SUBMIT_PATH', 'submit/')

UPLOADED_FILENAME_MAXLENGTH = int(getattr(django_settings, 'UPLOADED_FILENAME_MAXLENGTH', 128))


def default_callback(request, submit):
    messages.add_message(request, messages.SUCCESS, "Success")

SUBMIT_CALLBACK = getattr(django_settings, 'SUBMIT_CALLBACK', default_callback)
