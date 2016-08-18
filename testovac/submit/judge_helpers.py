import os
import time
import socket
import xml.etree.ElementTree as ET
from decimal import Decimal
from unidecode import unidecode

from django.utils.module_loading import import_string

from .constants import JudgeTestResult, ReviewResponse
from . import settings as submit_settings
from .submit_helpers import write_chunks_to_file
from .models import Review


class JudgeConnectionError(Exception):
    pass


def send_to_judge(review):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((submit_settings.JUDGE_ADDRESS, submit_settings.JUDGE_PORT))
        with open(review.raw_path(), 'rb') as raw:
            sock.send(raw.read())
    except:
        raise JudgeConnectionError
    finally:
        sock.close()


def create_review_and_send_to_judge(submit):
    review = Review(submit=submit, score=0, short_response=ReviewResponse.SENDING_TO_JUDGE)
    review.save()
    prepare_raw_file(review)
    try:
        send_to_judge(review)
        review.short_response = ReviewResponse.SENT_TO_JUDGE
    except JudgeConnectionError:
        review.short_response = ReviewResponse.JUDGE_UNAVAILABLE
        raise JudgeConnectionError
    finally:
        review.save()


def prepare_raw_file(review):
    with open(review.submit.file_path(), 'rb') as submitted_file:
        submitted_source = submitted_file.read()

    review_id = str(review.id)
    user_id = '%s-%s' % (submit_settings.JUDGE_INTERFACE_IDENTITY, str(review.submit.user.id))

    original_filename = unidecode(review.submit.filename)
    receiver_id = review.submit.receiver.configuration.get('inputs_folder_at_judge', None) \
                  or import_string(submit_settings.JUDGE_DEFAULT_INPUTS_FOLDER_FOR_RECEIVER)(review.submit.receiver)

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


def parse_protocol(protocol_path, force_show_details=False):
    data = dict()
    data['ready'] = True

    try:
        tree = ET.parse(protocol_path)
    except:
        # Protocol is either corrupted or just upload is not finished
        data['ready'] = False
        return data

    clog = tree.find('compileLog')
    data['compile_log_present'] = clog is not None
    data['compile_log'] = clog.text if clog is not None else ''

    tests = []
    runlog = tree.find('runLog')
    if runlog is not None:
        for runtest in runlog:
            # Test log format in protocol is: name, resultCode, resultMsg, time, details
            if runtest.tag != 'test':
                continue
            test = dict()
            test['name'] = runtest[0].text
            test['result'] = runtest[2].text
            test['time'] = runtest[3].text
            details = runtest[4].text if len(runtest) > 4 else None
            test['details'] = details
            test['show_details'] = details is not None and ('sample' in test['name'] or force_show_details)
            tests.append(test)
    data['tests'] = tests
    data['have_tests'] = len(tests) > 0

    try:
        data['score'] = Decimal(tree.find('runLog/score').text)
    except:
        data['score'] = 0

    if data['compile_log_present']:
        data['final_result'] = JudgeTestResult.COMPILATION_ERROR
    else:
        data['final_result'] = JudgeTestResult.OK
        for test in data['tests']:
            if test['result'] != JudgeTestResult.OK:
                data['final_result'] = test['result']
                break

    return data
