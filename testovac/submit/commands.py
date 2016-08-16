from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from . judge_helpers import create_review_and_send_to_judge, JudgeConnectionError
from . models import Submit, SubmitReceiver


def rejudge_submit(request, submit_id):
    submit = get_object_or_404(Submit.objects.select_related('receiver'), pk=submit_id)

    if not submit.receiver.has_admin_privileges(request.user):
        raise PermissionDenied

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
    For selected receiver send each accepted (acc. with penalization) submit of each user to judge.
    """
    receiver = get_object_or_404(SubmitReceiver, pk=receiver_id)

    if not receiver.has_admin_privileges(request.user):
        raise PermissionDenied

    if not receiver.configuration.get('send_to_judge', False):
        raise Http404

    submits = Submit.objects\
        .filter(receiver__id=receiver_id, is_accepted__in=[Submit.ACCEPTED, Submit.ACCEPTED_WITH_PENALIZATION])\
        .order_by('time', 'pk')

    failed_submits = []
    for submit in submits:
        try:
            create_review_and_send_to_judge(submit)
        except:
            failed_submits.append(submit)

    if failed_submits:
        messages.add_message(request, messages.ERROR, u"{}: {}".format(_('Failed submits'), map(str, failed_submits)))
    else:
        messages.add_message(request, messages.SUCCESS, _('Everything OK'))

    return redirect('/')
