from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from testovac.results.models import CustomResultsTable
from testovac.tasks.models import Contest, Competition


def results_index(request):
    custom_tables = CustomResultsTable.objects.order_by('number')
    custom_tables_data = []
    for custom_table in custom_tables:
        custom_tables_data.append({
            'custom_table': custom_table,
            'task_list': custom_table.task_list(request.user),
        })

    contests = Competition.objects.get(pk=settings.CURRENT_COMPETITION_PK).contests.all()
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
        {'contest': contest, 'task_list': [task for task in contest.task_set.all()]}
    )


def custom_results(request, results_table_slug):
    results_table = get_object_or_404(CustomResultsTable, pk=results_table_slug)
    task_list = results_table.task_list(request.user)
    return render(
        request,
        'results/custom_results_table.html',
        {'task_list': task_list, 'table_object': results_table},
    )
