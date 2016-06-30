from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .models import SubmitReceiver, Submit
from .forms import FileSubmitForm
from .submit_helpers import create_submit, send_to_judge
from django.views.generic import View


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
            if 'send_to_judge' in config and config['send_to_judge']:
                self.send_to_judge(submit)
            messages.add_message(request, messages.SUCCESS, self.get_success_message(submit))
        else:
            for field in form:
                for error in field.errors:
                    messages.add_message(request, messages.ERROR, "%s: %s" % (field.label, error))

            for error in form.non_field_errors():
                messages.add_message(request, messages.ERROR, error)

        if 'redirect_to' in request.POST and request.POST['redirect_to']:
            return redirect(request.POST['redirect_to'])
        else:
            return redirect('/')


@login_required
def view_submit(request, submit_id):
    submit = get_object_or_404(Submit, pk=submit_id)
    if submit.user != request.user and not request.user.is_staff:
        raise PermissionDenied()

    data = {
        'submit': submit,
        'review': submit.last_review(),
    }

    return render(request, 'submit/view_submit.html', data)
