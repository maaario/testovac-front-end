from django import template

from ..forms import SourceSubmitForm, DescriptionSubmitForm, TestableZipSubmitForm
from ..models import Submit

register = template.Library()


@register.inclusion_tag('submit/parts/submit_form.html')
def show_submit_form(receiver, redirect):
    """
    Renders submit form for specified task.
    """
    data = {
        'receiver': receiver,
        'redirect_to': redirect,
        'Submit': Submit,
    }
    if receiver.has_source:
        data['source_form'] = SourceSubmitForm()
    if receiver.has_description:
        data['description_form'] = DescriptionSubmitForm()
    if receiver.has_testable_zip:
        data['testable_zip_form'] = TestableZipSubmitForm()
    return data


@register.inclusion_tag('submit/parts/submit_list.html')
def show_submit_list(receiver, user):
    """
    Renders submit list for specified receiver and user.
    """
    data = {}
    return data
