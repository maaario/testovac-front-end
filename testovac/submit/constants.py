from django.utils.translation import ugettext_lazy as _

SUBMITTED_FILE_EXTENSION = '.submit'
REVIEWED_FILE_EXTENSION = '.review'
TESTING_PROTOCOL_EXTENSION = '.protocol'
TESTING_RAW_EXTENSION = '.raw'
DEDUCE_LANGUAGE_AUTOMATICALLY_OPTION = '.'


class JudgeTestResult(object):
    """
    Groups all common values of test results in protocol.
    Stores verbose versions of results.
    """
    OK = 'OK'
    WRONG_ANSWER = 'WA'
    TIME_LIMIT_EXCEEDED = 'TLE'
    RUNTIME_EXCEPTION = 'EXC'
    SECURITY_EXCEPTION = 'SEC'
    IGNORED = 'IGN'
    COMPILATION_ERROR = 'CERR'

    VERBOSE_RESULT = {
        OK: _('OK'),
        WRONG_ANSWER: _('Wrong answer'),
        TIME_LIMIT_EXCEEDED: _('Time limit exceeded'),
        RUNTIME_EXCEPTION: _('Runtime exception'),
        SECURITY_EXCEPTION: _('Security exception'),
        IGNORED: _('Ignored'),
        COMPILATION_ERROR: _('Compilation error'),
    }

    @classmethod
    def verbose(cls, result):
        return cls.VERBOSE_RESULT.get(result, result)


class ReviewResponse(JudgeTestResult):
    """
    Groups all common values of Review.short_response.
    Stores verbose versions of responses.
    """

    SENDING_TO_JUDGE = 'Sending to judge'
    SENT_TO_JUDGE = 'Sent to judge'
    JUDGE_UNAVAILABLE = 'Judge unavailable'
    REVIEWED = 'Reviewed'

    VERBOSE_RESPONSE = {
        SENDING_TO_JUDGE: _(SENDING_TO_JUDGE),
        SENT_TO_JUDGE: _(SENT_TO_JUDGE),
        JUDGE_UNAVAILABLE: _(JUDGE_UNAVAILABLE),
        REVIEWED: _(REVIEWED),
    }

    @classmethod
    def verbose(cls, response):
        if response in cls.VERBOSE_RESPONSE:
            return cls.VERBOSE_RESPONSE[response]
        return cls.VERBOSE_RESULT.get(response, response)
