from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from . judge_helpers import create_review_and_send_to_judge, JudgeConnectionError
from . models import Submit, SubmitReceiver


def rejudge_submit(request, submit_id):
    if not request.user.is_staff:
        raise PermissionDenied

    submit = get_object_or_404(Submit, pk=submit_id)
    if not submit.receiver.configuration.get('send_to_judge', False):
        raise Http404

    try:
        create_review_and_send_to_judge(submit)
        messages.add_message(request, messages.SUCCESS, _('Resubmit successful.'))
    except JudgeConnectionError:
        messages.add_message(request, messages.ERROR, _('Resubmit not successful. Judge unavailable.'))

    return redirect(submit.get_absolute_url())


def rejudge_receiver_submits(request, receiver_id):
    """
    For selected receiver send last accepted (acc. with penalization) submit of each user to judge.
    """
    if not request.user.is_staff:
        raise PermissionDenied

    receiver = get_object_or_404(SubmitReceiver, pk=receiver_id)
    if not receiver.configuration.get('send_to_judge', False):
        raise Http404

    submits = Submit.objects\
        .filter(receiver__id=receiver_id, is_accepted__in=[Submit.ACCEPTED, Submit.ACCEPTED_WITH_PENALIZATION])\
        .order_by('-time')
    users_rejudged = set()

    failed_submits = []
    for submit in submits:
        if submit.user not in users_rejudged:
            try:
                users_rejudged.add(submit.user)
                create_review_and_send_to_judge(submit)
            except:
                failed_submits.append(submit)

    if failed_submits:
        messages.add_message(request, messages.ERROR, u"{}: {}".format(_('Failed submits'), map(str, failed_submits)))
    else:
        messages.add_message(request, messages.SUCCESS, _('Everything OK'))

    return redirect('/')
