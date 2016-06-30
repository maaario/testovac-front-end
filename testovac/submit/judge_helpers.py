import os
import time
import socket

from .models import Review
from . import settings as submit_settings
from .submit_helpers import write_chunks_to_file


def send_to_judge(submit):
    review = Review(submit=submit, score=0, short_response='sending to judge')
    review.save()
    prepare_raw_file(review)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('127.0.0.1', 12347))
    except socket.error:
        review.short_response = 'judge unavailable'
        review.save()
        raise Exception

    with open(review.raw_path(), 'r') as raw:
        sock.send(raw.read())
    sock.close()

    review.short_response = 'sent to judge'
    review.save()


def prepare_raw_file(review):
    with open(review.submit.file_path(), 'r') as submitted_file:
        submitted_source = submitted_file.read()

    review_id = str(review.id)
    user_id = submit_settings.JUDGE_INTERFACE_IDENTITY + '-' + str(review.submit.user.username)

    original_filename = review.submit.filename
    receiver_id = str(review.submit.receiver.id)
    language = os.path.splitext(original_filename)[1]
    correct_filename = receiver_id + language

    timestamp = int(time.time())

    raw_head = "%s\n%s\n%s\n%s\n%d\n%s\n" % (
        submit_settings.JUDGE_INTERFACE_IDENTITY,
        review_id,
        user_id,
        correct_filename,
        timestamp,
        original_filename,
    )

    write_chunks_to_file(review.raw_path(), [raw_head, submitted_source])
