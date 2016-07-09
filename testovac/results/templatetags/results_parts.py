from django import template

from testovac.results.table_generator import generate_result_table
from testovac.results.task_points import display_points

register = template.Library()


@register.filter
def points_format(points):
    return display_points(points)


@register.inclusion_tag('results/parts/results_table.html')
def results_table(tasks):
    max_sum = sum(tasks.values_list('max_points', flat=True))
    table_data = generate_result_table(tasks)
    return {'tasks': tasks, 'table_data': table_data, 'max_sum': max_sum}
