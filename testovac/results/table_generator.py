from itertools import chain

from django.contrib.auth.models import User

from testovac.results.task_points import user_task_points
from testovac.submit.models import Submit


def generate_result_table(tasks):
    def users():
        receivers = [task.submit_receivers.values_list('pk', flat=True) for task in tasks]
        user_ids = Submit.objects\
            .filter(receiver__in=chain(*receivers),
                    is_accepted__in=[Submit.ACCEPTED, Submit.ACCEPTED_WITH_PENALIZATION])\
            .values_list('user', flat=True)
        return User.objects.filter(pk__in=set(user_ids))

    def create_table_row(user):
        row_data = {
            'user': user,
            'is_ranked': not user.is_staff,
            'task_points': [user_task_points(task, user) for task in tasks],
        }
        row_data['sum'] = sum(row_data['task_points'])
        return row_data

    def calculate_ranking(table):
        current_rank = None
        next_rank = 1
        last_score = None
        for row_data in table:
            if not row_data['is_ranked']:
                row_data['rank'] = None
                continue
            if row_data['sum'] != last_score:
                current_rank = next_rank
                last_score = row_data['sum']
            next_rank += 1
            row_data['rank'] = current_rank

    table = [create_table_row(user) for user in users()]
    table = sorted(table, key=lambda r: r['sum'], reverse=True)
    calculate_ranking(table)
    return table
