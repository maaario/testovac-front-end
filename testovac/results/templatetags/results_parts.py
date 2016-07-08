from django import template

from testovac.results.task_points import display_points

register = template.Library()


@register.filter
def points_format(points):
    return display_points(points)
