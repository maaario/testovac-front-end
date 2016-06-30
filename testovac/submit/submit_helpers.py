import os

from .models import Submit
from . import settings as submit_settings
import constants


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

