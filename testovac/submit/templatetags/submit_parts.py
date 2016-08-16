from django import template

from ..constants import ReviewResponse
from ..forms import FileSubmitForm
from ..models import Review, Submit

register = template.Library()


@register.inclusion_tag('submit/parts/submit_form.html')
def submit_form(receiver, redirect, user, caption=None):
    """
    Renders submit form (or link) for specified SubmitReceiver.
    If the receiver doesn't have form (or link), nothing will be rendered.
    """
    data = {
        'user_can_post_submit': receiver.can_post_submit(user),
        'receiver': receiver,
        'redirect_to': redirect,
    }

    conf = receiver.configuration
    if 'form' in conf:
        data['submit_form'] = FileSubmitForm(configuration=conf['form'])
        data['caption'] = conf['form'].get('caption', None) or caption
    if 'link' in conf:
        data['submit_link'] = conf['link']

    return data


@register.inclusion_tag('submit/parts/submit_list.html')
def submit_list(receiver, user):
    """
    List of all submits for specified user and receiver.
    """

    last_review_for_each_submit = Review.objects.filter(
        submit__receiver=receiver, submit__user=user
    ).order_by(
        '-submit__pk', '-time', '-pk'
    ).distinct(
        'submit__pk'
    ).select_related(
        'submit'
    )

    data = {
        'user_has_admin_privileges': receiver.has_admin_privileges(user),
        'receiver': receiver,
        'submits': [(review.submit, review) for review in last_review_for_each_submit],
        'response': ReviewResponse,
        'Submit': Submit,
    }
    return data


@register.filter
def verbose(obj, msg):
    """
    Use to print verbose versions of constants.JudgeTestResult
    """
    return obj.verbose(msg)
