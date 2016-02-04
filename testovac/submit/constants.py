from django.utils.translation import ugettext_lazy as _

SUBMIT_RAW_FILE_EXTENSION = '.raw'
SUBMIT_SOURCE_FILE_EXTENSION = '.data'
SUBMIT_PROTOCOL_FILE_EXTENSION = '.protocol'

SUBMIT_VERBOSE_TESTER_RESPONSE = {
    'WA': _('Wrong answer'),
    'CERR': _('Compilation error'),
    'TLE': _('Time limit exceeded'),
    'OK': _('OK'),
    'EXC': _('Runtime exception'),
    'SEC': _('Security exception'),
}
