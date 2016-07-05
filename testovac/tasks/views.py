from django.shortcuts import render, get_object_or_404
from django.http import Http404

from testovac.tasks.models import Contest, Task


def contest_list(request):
    contests = Contest.objects.order_by('number')
    template_data = {
        'contests': (contest for contest in contests if contest.is_visible_for_user(request.user))
    }
    return render(
        request,
        'tasks/contest_list.html',
        template_data,
    )


def task_statement(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not task.is_visible_for_user(request.user):
        raise Http404
    template_data = {
        'task': task,
    }
    return render(
        request,
        'tasks/task_statement.html',
        template_data,
    )
