from django import template

from ..forms import FileSubmitForm

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
