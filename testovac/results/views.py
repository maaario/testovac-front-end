from django.http import Http404
from django.shortcuts import get_object_or_404, render

from testovac.results.table_generator import generate_result_table
from testovac.results.models import CustomResultsTable
from testovac.tasks.models import Contest, Task


def contest_results(request, contest_slug):
    contest = get_object_or_404(Contest, pk=contest_slug)
    if not contest.is_visible_for_user(request.user):
        raise Http404
    tasks = contest.task_set.all()
    max_sum = sum(tasks.values_list('max_points', flat=True))
    table_data = generate_result_table(tasks)
    return render(
        request,
        'results/contest_results_table.html',
        {'contest': contest, 'tasks': tasks, 'table_data': table_data, 'max_sum': max_sum}
    )


def custom_results(request, results_table_slug):
    results_table = get_object_or_404(CustomResultsTable, pk=results_table_slug)

    task_pks = []
    for contest in results_table.contests.all():
        if contest.is_visible_for_user(request.user):
            task_pks.extend(contest.task_set.all().values_list('pk', flat=True))
    tasks = Task.objects.filter(pk__in=task_pks).order_by('-contest__number', 'number')
    max_sum = sum(tasks.values_list('max_points', flat=True))
    table_data = generate_result_table(tasks)
    return render(
        request,
        'results/custom_results_table.html',
        {'custom_table': results_table, 'tasks': tasks, 'table_data': table_data, 'max_sum': max_sum}
    )
