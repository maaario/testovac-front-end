from django import template

from ..forms import FileSubmitForm
from ..models import Submit

register = template.Library()


@register.inclusion_tag('submit/parts/submit_form.html')
def submit_form(receiver, redirect):
    """
    Renders submit form for specified SubmitReceiver.
    """
    data = {
        'receiver': receiver,
        'redirect_to': redirect,
    }

    conf = receiver.configuration
    if 'form' in conf:
        data['submit_form'] = FileSubmitForm(configuration=conf['form'])
    if 'link' in conf:
        data['submit_link'] = conf['link']

    return data


@register.inclusion_tag('submit/parts/submit_list.html')
def submit_list(receiver, user):
    submits = Submit.objects.filter(receiver=receiver, user=user)
    data = {
        'submits': [(submit, submit.last_review()) for submit in submits]
    }
    return data
