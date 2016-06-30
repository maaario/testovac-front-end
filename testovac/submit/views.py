import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import SubmitReceiver, Submit, Review
from .forms import FileSubmitForm
from .submit_helpers import create_submit, write_chunks_to_file, send_file
from .judge_helpers import send_to_judge


class PostSubmitForm(View):
    login_required = True

    def can_post_submit(self, receiver, user):
        """
        Override this method to set, who can submit to this receiver.
        E.g. users not allowed in this competition can't submit solutions for this task.
        """
        return True

    def is_submit_accepted(self, submit):
        """
        Override this method to decide which submits will be accepted, penalized or not accepted.
        This method is called after the submit is created, but before it is saved in database.
        E.g. submits after deadline are not accepted.
        """
        return Submit.ACCEPTED

    def get_success_message(self, submit):
        """
        This message will be added to `messages` after successful submit.
        """
        return 'Success'

    def send_to_judge(self, submit):
        """
        Override if you use a different judge.
        """
        send_to_judge(submit)

    def redirect_after_post(self, request):
        """
        Override to redirect to a different location after submit.
        """
        if 'redirect_to' in request.POST and request.POST['redirect_to']:
            return request.POST['redirect_to']
        else:
            return '/'

    def post(self, request, receiver_id):
        receiver = get_object_or_404(SubmitReceiver, pk=receiver_id)
        config = receiver.configuration

        if not self.can_post_submit(receiver, request.user):
            raise PermissionDenied()

        if 'form' in config:
            form = FileSubmitForm(request.POST, request.FILES, configuration=config['form'])
        else:
            raise PermissionDenied()

        if form.is_valid():
            submit = create_submit(user=request.user,
                                   receiver=receiver,
                                   is_accepted_method=self.is_submit_accepted,
                                   sfile=request.FILES['submit_file'],
                                   )
        else:
            for field in form:
                for error in field.errors:
                    messages.add_message(request, messages.ERROR, "%s: %s" % (field.label, error))
            for error in form.non_field_errors():
                messages.add_message(request, messages.ERROR, error)
            return redirect(self.redirect_after_post(request))

        if 'send_to_judge' in config and config['send_to_judge']:
            try:
                self.send_to_judge(submit)
            except Exception:
                messages.add_message(request, messages.ERROR, 'Upload to judge was not successful.')
                return redirect(self.redirect_after_post(request))

        messages.add_message(request, messages.SUCCESS, self.get_success_message(submit))
        return redirect(self.redirect_after_post(request))


@login_required
def view_submit(request, submit_id):
    submit = get_object_or_404(Submit, pk=submit_id)
    if submit.user != request.user and not request.user.is_staff:
        raise PermissionDenied()

    review = submit.last_review()
    data = {
        'submit': submit,
        'review': review,
    }

    return render(request, 'submit/view_submit.html', data)


@login_required
def download_submit(request, submit_id):
    submit = get_object_or_404(Submit, pk=submit_id)
    if submit.user != request.user and not request.user.is_staff:
        raise PermissionDenied()
    return send_file(request, submit.file_path(), submit.filename)


@login_required
def download_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.submit.user != request.user and not request.user.is_staff:
        raise PermissionDenied()
    return send_file(request, review.file_path(), review.filename)


@csrf_exempt
@require_POST
def receive_protocol(request):
    review_id = request.POST['submit_id']
    review = get_object_or_404(Review, pk=review_id)
    review.short_response = request.POST['result']
    write_chunks_to_file(review.protocol_path(), [request.POST['log']])
    review.save()
    return HttpResponse("")
