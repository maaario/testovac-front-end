from django import template

from ..constants import ReviewResponse
from ..forms import FileSubmitForm
from ..models import Submit

register = template.Library()


@register.inclusion_tag('submit/parts/submit_form.html')
def submit_form(receiver, redirect, caption=None):
    """
    Renders submit form for specified SubmitReceiver.
    """
    data = {
        'receiver': receiver,
        'redirect_to': redirect,
        'caption': caption,
    }

    conf = receiver.configuration
    if 'form' in conf:
        data['submit_form'] = FileSubmitForm(configuration=conf['form'])
    if 'link' in conf:
        data['submit_link'] = conf['link']

    return data


@register.inclusion_tag('submit/parts/submit_list.html')
def submit_list(receiver, user):
    submits = Submit.objects.filter(receiver=receiver, user=user).order_by('-time')
    data = {
        'submits': [(submit, submit.last_review()) for submit in submits],
        'response': ReviewResponse,
    }
    return data


@register.filter
def verbose(obj, msg):
    """
    Use to print verbose versions of constants.JudgeTestResult
    """
    return obj.verbose(msg)
