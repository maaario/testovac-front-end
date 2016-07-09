from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.module_loading import import_string

from testovac.tasks.models import Contest, Task


def contest_list(request):
    contests = Contest.objects.order_by('-number')
    visible_contests = [contest for contest in contests if contest.is_visible_for_user(request.user)]

    receiver_lists = [contest.all_submit_receivers().values_list('id', flat=True) for contest in visible_contests]
    receiver_lists_as_strings = map(lambda l: ','.join(map(str, l)), receiver_lists)

    template_data = {
        'contests_with_receivers': zip(visible_contests, receiver_lists_as_strings)
    }
    return render(
        request,
        'tasks/contest_list.html',
        template_data,
    )


def task_statement(request, task_slug):
    task = get_object_or_404(Task, pk=task_slug)
    if not task.contest.tasks_visible_for_user(request.user):
        raise Http404
    template_data = {
        'task': task,
        'statement': import_string(settings.TASK_STATEMENTS_BACKEND)().render_statement(request, task),
    }
    return render(
        request,
        'tasks/task_statement.html',
        template_data,
    )


def task_statement_download(request, task_slug):
    task = get_object_or_404(Task, pk=task_slug)
    if not task.contest.tasks_visible_for_user(request.user):
        raise Http404
    return import_string(settings.TASK_STATEMENTS_BACKEND)().download_statement(request, task)
