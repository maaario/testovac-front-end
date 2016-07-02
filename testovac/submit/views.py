from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .constants import JudgeTestResult, ReviewResponse
from .models import SubmitReceiver, Submit, Review
from .forms import FileSubmitForm
from .submit_helpers import create_submit, write_chunks_to_file, send_file
from .judge_helpers import prepare_raw_file, send_to_judge, parse_protocol


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
        if submit.receiver.configuration.get('send_to_judge', False):
            return format_html(
                    _('Submit successful. Testing protocol will be soon available <a href="{link}">here</a>.'),
                    link=reverse('view_submit', args=[submit.id])
            )
        return _('Submit successful.')

    def send_to_judge(self, submit):
        review = Review(submit=submit, score=0, short_response=ReviewResponse.SENDING_TO_JUDGE)
        review.save()
        prepare_raw_file(review)
        try:
            send_to_judge(review)
            review.short_response = ReviewResponse.SENT_TO_JUDGE
        except:
            review.short_response = ReviewResponse.JUDGE_UNAVAILABLE
            raise Exception
        finally:
            review.save()

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
            return redirect(request.POST['redirect_to'])

        if config.get('send_to_judge', False):
            try:
                self.send_to_judge(submit)
            except:
                messages.add_message(request, messages.ERROR, _('Upload to judge was not successful.'))
                return redirect(request.POST['redirect_to'])

        messages.add_message(request, messages.SUCCESS, self.get_success_message(submit))
        return redirect(request.POST['redirect_to'])


@login_required
def view_submit(request, submit_id):
    submit = get_object_or_404(Submit, pk=submit_id)
    if submit.user != request.user and not request.user.is_staff:
        raise PermissionDenied()

    conf = submit.receiver.configuration
    review = submit.last_review()
    data = {
        'submit': submit,
        'review': review,
        'protocol_expected': conf.get('send_to_judge', False),
        'show_submitted_file': conf.get('send_to_judge', False) and not conf.get('testable_zip', False),
    }

    if data['show_submitted_file']:
        with open(submit.file_path(), 'r') as submitted_file:
            data['submitted_file'] = submitted_file.read().decode('utf-8', 'replace')

    if data['protocol_expected'] and review and review.protocol_exists():
        force_show_details = conf.get('testable_zip', False) or request.user.is_staff
        data['protocol'] = parse_protocol(review.protocol_path(), force_show_details)
        data['result'] = JudgeTestResult

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
    write_chunks_to_file(review.protocol_path(), [request.POST['protocol']])

    protocol_data = parse_protocol(review.protocol_path())
    review.score = protocol_data['score']
    review.short_response = protocol_data['final_result']
    review.save()

    return HttpResponse("")
