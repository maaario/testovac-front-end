from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect

from .models import SubmitReceiver, Submit
from .forms import FileSubmitForm
from .submit_helpers import write_chunks_to_file
from . import settings as submit_settings


@login_required
@require_POST
def post_submit(request, receiver_id):
    receiver = get_object_or_404(SubmitReceiver, pk=receiver_id)
    config = receiver.configuration

    form = FileSubmitForm(request.POST, request.FILES, configuration=config['form'])
    if form.is_valid():
        sfile = request.FILES['submit_file']

        submit = Submit(receiver=receiver,
                        user=request.user,
                        filename=sfile.name)
        submit_settings.SUBMIT_CALLBACK(request, submit)

        submit.save()

        write_chunks_to_file(submit.file_path(), sfile.chunks())

        if 'send_to_judge' in config and config['send_to_judge']:
            pass
    else:
        for field in form:
            for error in field.errors:
                messages.add_message(request, messages.ERROR, "%s: %s" % (field.label, error))

    if 'redirect_to' in request.POST and request.POST['redirect_to']:
        return redirect(request.POST['redirect_to'])
    else:
        return redirect('/')
