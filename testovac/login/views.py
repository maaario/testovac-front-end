from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from testovac.login.forms import ExtendedUserCreationForm


def add_form_errors_to_messages(request, form):
    for field in form:
        for error in field.errors:
            messages.add_message(request, messages.ERROR, u"%s: %s" % (field.label, error))
    for error in form.non_field_errors():
        messages.add_message(request, messages.ERROR, error)


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
            add_form_errors_to_messages(request, form)

    return HttpResponseRedirect(problem_redirect)


def register(request):
    if request.user.is_authenticated():
        return redirect('contest_list')

    already_filled = {field_name: '' for field_name in ('username', 'first_name', 'last_name', 'email')}

    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
            auth_login(request, user)
            messages.success(request, _('Thanks for registering. You are now logged in.'))
            return redirect('login')
        else:
            add_form_errors_to_messages(request, form)
            for field_name in already_filled:
                already_filled[field_name] = request.POST.get(field_name)

    return render(request, "login/registration.html", {'form': ExtendedUserCreationForm(initial=already_filled)})
