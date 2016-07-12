from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.module_loading import import_string

from testovac.tasks.models import Competition, Task
from testovac.results.generator import ResultsGenerator


def contest_list(request):
    visible_contests = Competition.objects.get(pk=settings.CURRENT_COMPETITION_PK).get_visible_contests(request.user)
    visible_contests = visible_contests.prefetch_related('task_set__submit_receivers')

    receiver_lists_as_strings = []
    for contest in visible_contests:
        receivers = []
        for task in contest.task_set.all():
            for receiver in task.submit_receivers.all():
                receivers.append(receiver.pk)
        receivers_string = ','.join(map(str, receivers))
        receiver_lists_as_strings.append(receivers_string)

    template_data = {
        'contests_with_receivers': zip(visible_contests, receiver_lists_as_strings),
        'user_task_points': ResultsGenerator(
            User.objects.filter(pk=request.user.pk), Task.objects.filter(contest__in=visible_contests)
        ).get_user_task_points()
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
        'user_task_points': ResultsGenerator(
            User.objects.filter(pk=request.user.pk), (task, )).get_user_task_points(),
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
