from django import template

from testovac.results.table_generator import generate_result_table
from testovac.results.task_points import display_points
from testovac.utils import is_true

register = template.Library()


@register.filter
def points_format(points):
    return display_points(points)


@register.inclusion_tag('results/parts/results_table.html', takes_context=True)
def results_table(context, tasks):
    request = context['request']
    max_sum = sum(tasks.values_list('max_points', flat=True))
    table_data = generate_result_table(tasks)
    return {
        'tasks': tasks,
        'table_data': table_data,
        'max_sum': max_sum,
        'show_staff': is_true(request.GET.get('show_staff', request.user.is_staff)),
        'user': request.user,
    }