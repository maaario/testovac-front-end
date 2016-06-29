import os

from .models import Submit


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


def send_to_judge(submit):
    pass
