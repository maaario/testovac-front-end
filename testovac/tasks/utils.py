from django.utils import timezone


def default_contest_start_end_time():
    return timezone.now().replace(minute=0, second=0, microsecond=0)
