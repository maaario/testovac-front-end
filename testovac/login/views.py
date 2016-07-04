from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    """
    Displays the login form and handles the login action.
    """
    success_redirect = reverse('contest_list')
    problem_redirect = reverse('wiki:root')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=success_redirect, host=request.get_host()):
                return HttpResponseRedirect(problem_redirect)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(success_redirect)
        else:
            for field in form:
                for error in field.errors:
                    messages.add_message(request, messages.ERROR, "%s: %s" % (field.label, error))
            for error in form.non_field_errors():
                messages.add_message(request, messages.ERROR, error)

    return HttpResponseRedirect(problem_redirect)
