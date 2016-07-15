from collections import defaultdict

from testovac.submit.models import Submit, Review
from testovac.tasks.models import Task


class ResultsGenerator(object):
    @classmethod
    def score_to_points(cls, scores, task):
        """
        :param scores: a dictionary receiver.pk -> score/None for receiver
        :param task: a task object with prefetched receivers

        This function calculates the final task points from review.score.

        This implementation treats all submit receivers as equal - task points are split between them equally.
        """
        sum_of_scores = 0
        for receiver in task.submit_receivers.all():
            if scores[receiver.pk] is not None:
                sum_of_scores += scores[receiver.pk]
        return round(sum_of_scores / (100 * len(task.submit_receivers.all())) * task.max_points, 2)

    def __init__(self, users, task_list):
        self.users = users
        self.task_list = task_list

    def reviews_to_final_points(self, receiver_reviews, task):
        """
        :param receiver_reviews: a dictionary receiver.pk -> list of reviews for specific user and task.receiver
        :param task: a task object with prefetched receivers

        From lists (one list per receiver)
        of all reviews (last review for each accepted submit)
        calculates points for task for user.
        """
        score_for_receiver = defaultdict(lambda: None)
        for receiver in task.submit_receivers.all():
            if receiver_reviews[receiver.pk]:
                score_for_receiver[receiver.pk] = max((review.score for review in receiver_reviews[receiver.pk]))

        user_has_at_least_one_review = False
        for score in score_for_receiver:
            if score is not None:
                user_has_at_least_one_review = True

        if user_has_at_least_one_review:
            return self.score_to_points(score_for_receiver, task)
        else:
            return None

    def get_user_task_points(self):
        """
        For each user and task gets a list of all reviews (last review for each accepted submit).
        Then calculates task points via `reviews_to_final_points`
        Returns a dictionary [user.pk][task.pk] -> points.
        """
        tasks_with_receivers = Task.objects.filter(
            pk__in=[task.pk for task in self.task_list]
        ).prefetch_related('submit_receivers')

        receivers = set((receiver.pk for task in tasks_with_receivers for receiver in task.submit_receivers.all()))

        reviews = Review.objects.filter(
            submit__receiver__in=receivers
        ).filter(
            submit__user__in=self.users
        ).filter(
            submit__is_accepted__in=[Submit.ACCEPTED, Submit.ACCEPTED_WITH_PENALIZATION]
        ).order_by(
            'submit__pk', '-time', '-pk'
        ).distinct(
            'submit__pk'
        ).select_related('submit__user', 'submit__receiver')

        tasks_for_receiver = defaultdict(list)
        for task in tasks_with_receivers:
            for receiver in task.submit_receivers.all():
                tasks_for_receiver[receiver.pk].append(task)

        user_task_receiver_reviews = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for review in reviews:
            for task in tasks_for_receiver[review.submit.receiver.pk]:
                user_task_receiver_reviews[review.submit.user.pk][task.pk][review.submit.receiver.pk].append(review)

        user_task_points = defaultdict(lambda: defaultdict(lambda: None))
        for user in self.users:
            for task in tasks_with_receivers:
                user_task_points[user.pk][task.pk] = self.reviews_to_final_points(
                    receiver_reviews=user_task_receiver_reviews[user.pk][task.pk], task=task
                )

        return user_task_points

    def generate_result_table_context(self):
        def create_table_row(user, task_points):
            row_data = {
                'user': user,
                'is_ranked': not user.is_staff,
                'task_points': [task_points[task.pk] for task in self.task_list],
            }
            row_data['sum'] = sum((points for points in row_data['task_points'] if points is not None))
            return row_data

        def row_non_empty(row):
            for points in row['task_points']:
                if points is not None:
                    return True
            return False

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

        user_task_points = self.get_user_task_points()
        table = [create_table_row(user, user_task_points[user.pk]) for user in self.users]
        table = list(filter(row_non_empty, table))
        table = sorted(table, key=lambda r: r['sum'], reverse=True)
        calculate_ranking(table)
        return table


def display_points(points):
    if points is None:
        return ""
    return "{:.2f}".format(points)
