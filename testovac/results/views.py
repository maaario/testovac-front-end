from django.http import Http404
from django.shortcuts import get_object_or_404, render

from testovac.results.models import CustomResultsTable
from testovac.tasks.models import Contest, Task


def results_index(request):
    custom_tables = CustomResultsTable.objects.order_by('number')
    custom_tables_data = []
    for custom_table in custom_tables:
        custom_tables_data.append({
            'custom_table': custom_table,
            'tasks': custom_table.tasks(request.user),
        })

    contests = Contest.objects.order_by('-number')
    visible_contests = [contest for contest in contests if contest.tasks_visible_for_user(request.user)]

    return render(
        request,
        'results/results_index.html',
        {'custom_tables': custom_tables_data, 'contests': visible_contests}
    )


def contest_results(request, contest_slug):
    contest = get_object_or_404(Contest, pk=contest_slug)
    if not contest.tasks_visible_for_user(request.user):
        raise Http404
    return render(
        request,
        'results/contest_results_table.html',
        {'contest': contest}
    )


def custom_results(request, results_table_slug):
    results_table = get_object_or_404(CustomResultsTable, pk=results_table_slug)
    table_tasks = results_table.tasks(request.user)
    return render(
        request,
        'results/custom_results_table.html',
        {'table_tasks': table_tasks, 'table_object': results_table},
    )
