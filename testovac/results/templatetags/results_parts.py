from decimal import Decimal

from django import template
from django.contrib.auth.models import User

from testovac.results.generator import ResultsGenerator, display_points
from testovac.utils import is_true

register = template.Library()


@register.filter
def points_format(points):
    return display_points(points)


@register.inclusion_tag('results/parts/results_table.html', takes_context=True)
def results_table(context, task_list):
    request = context['request']
    max_sum = sum(task.max_points for task in task_list)
    table_data = ResultsGenerator(User.objects.all(), task_list).generate_result_table_context()
    return {
        'tasks': task_list,
        'table_data': table_data,
        'max_sum': max_sum,
        'show_staff': is_true(request.GET.get('show_staff', request.user.is_staff)),
        'user': request.user,
    }


@register.inclusion_tag('results/parts/completed_status.html')
def completed_status(task, user, user_task_points):
    if not user.is_authenticated():
        return {
            'render': False,
        }

    points = user_task_points[user.pk][task.pk] or 0

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
