from testovac.submit.models import Submit


def is_submit_accepted(submit):
    """
    Submits after the contest has finished are automatically set to `not accepted`.
    Submit.is_accepted can be modified manually however.
    """
    if not submit.receiver.task_set.all():
        return Submit.NOT_ACCEPTED
    task = submit.receiver.task_set.all()[0]

    if task.contest.has_finished():
        return Submit.NOT_ACCEPTED
    else:
        return Submit.ACCEPTED


def review_points(review, task=None):
    """
    Judge returns score in per cent format,
    human reviewers assign absolute score points.
    """
    if task is None:
        possible_tasks = review.submit.receiver.task_set.all()
        if not possible_tasks:
            return 0
        task = possible_tasks[0]

    if review.submit.receiver.configuration.get('send_to_judge', False):
        return round(review.score / 100 * task.max_points, 2)
    else:
        return review.score


def display_points(points):
    if points is None:
        return ""
    return "{:.2f}".format(points)
