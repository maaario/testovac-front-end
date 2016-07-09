from decimal import Decimal

from django import template

from testovac.results.table_generator import generate_result_table
from testovac.results.task_points import display_points, user_task_points
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


@register.inclusion_tag('results/parts/completed_status.html')
def completed_status(task, user):
    if not user.is_authenticated():
        return {
            'render': False,
        }

    points = user_task_points(task, user)
    if Decimal(points) == 0:
        level = 'danger'
    elif Decimal(points) >= Decimal(task.max_points):
        level = 'success'
    else:
        level = 'warning'

    return {
        'render': True,
        'points': display_points(points),
        'max': display_points(task.max_points),
        'level': level,
    }
