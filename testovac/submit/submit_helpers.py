import os

from django.http import Http404
from sendfile import sendfile

import constants
from . import settings as submit_settings
from .models import Submit


def add_language_preference_to_filename(filename, language_preference, allowed_languages):
    name, extension = os.path.splitext(filename)
    extension = extension.lower()

    if language_preference != constants.DEDUCE_LANGUAGE_AUTOMATICALLY_OPTION:
        extension = language_preference

    if extension in submit_settings.SUBMIT_EXTENSION_MAPPING_FOR_JUDGE:
        extension = submit_settings.SUBMIT_EXTENSION_MAPPING_FOR_JUDGE[extension]
    else:
        raise Exception

    if extension not in allowed_languages:
        raise Exception

    return ''.join((name, extension))


def write_chunks_to_file(file_path, chunks):
    try:
        os.makedirs(os.path.dirname(file_path))
    except os.error:
        pass

    with open(file_path, 'wb+') as destination:
        for chunk in chunks:
            destination.write(chunk)


def create_submit(user, receiver, is_accepted_method, sfile = None):
    submit = Submit(receiver=receiver,
                    user=user,
                    filename=None if sfile is None else sfile.name)
    submit.is_accepted = is_accepted_method(submit)
    submit.save()
    write_chunks_to_file(submit.file_path(), sfile.chunks())
    return submit


def send_file(request, filepath, filename):
    """
    Display .txt and .pdf files in browser, offer download for other files
    Returns a response object.
    """
    extension = os.path.splitext(filename)[1]
    as_attachment = extension.lower() not in submit_settings.SUBMIT_VIEWABLE_EXTENSIONS
    if os.path.exists(filepath):
        response = sendfile(
            request,
            filepath,
            attachment=as_attachment,
            attachment_filename=filename,
        )
        response['Content-Disposition'] = 'inline; filename="%s"' % filename
        return response
    else:
        raise Http404
