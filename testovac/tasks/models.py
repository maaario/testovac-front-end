from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from sortedm2m.fields import SortedManyToManyField

from testovac.tasks.utils import default_contest_start_end_time
from testovac.submit.models import SubmitReceiver


@python_2_unicode_compatible
class Contest(models.Model):
    """
    One round or competition event, consists of tasks.
    Holds information about deadline and visibility.
    """
    slug = models.SlugField(primary_key=True,
                            help_text='Must be unique among all contests, serves as part of URL.<br />'
                                      'Must only contain characters "a-zA-Z0-9_-".')
    name = models.CharField(max_length=128)
    start_time = models.DateTimeField(default=default_contest_start_end_time, blank=True, null=True)
    end_time = models.DateTimeField(default=default_contest_start_end_time, blank=True, null=True)
    visible = models.BooleanField(default=False)

    def has_started(self):
        return self.start_time is None or timezone.now() > self.start_time

    def has_finished(self):
        return self.end_time is not None and timezone.now() > self.end_time

    def is_running(self):
        return self.has_started() and not self.has_finished()

    def is_visible_for_user(self, user):
        return (
            user.is_superuser or
            user.is_staff or
            self.visible
        )

    def tasks_visible_for_user(self, user):
        return (
            user.is_superuser or
            user.is_staff or
            (self.is_visible_for_user(user) and self.has_started())
        )

    def all_submit_receivers(self):
        return SubmitReceiver.objects.filter(task__in=self.task_set.values_list('slug', flat=True))

    class Meta:
        verbose_name = _('contest')
        verbose_name_plural = _('contests')

    def __str__(self):
        return u'{} ({})'.format(self.name, self.slug)


class TaskManager(models.Manager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset().order_by('number')

    use_for_related_fields = True


@python_2_unicode_compatible
class Task(models.Model):
    """
    General task data not related to testing are defined here.
    """
    slug = models.SlugField(primary_key=True,
                            help_text='Must be unique among all tasks, serves as part of URL.<br />'
                                      'By default, task.slug is also used as a name of inputs folder at judge.<br />'
                                      'Must only contain characters "a-zA-Z0-9_-".')
    name = models.CharField(max_length=128)
    contest = models.ForeignKey(Contest)
    number = models.IntegerField()
    max_points = models.IntegerField()
    submit_receivers = models.ManyToManyField(SubmitReceiver)

    objects = TaskManager()

    def get_absolute_url(self):
        return reverse('testovac.tasks.views.task_statement', kwargs=dict(task_slug=self.slug))

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return u'{} ({})'.format(self.name, self.slug)


@python_2_unicode_compatible
class Competition(models.Model):
    """
    Independent competition, consists of contests.
    Competition can be made accessible only to specific group of users.
    """
    slug = models.SlugField(primary_key=True, help_text='Must be unique, serves as part of URL.<br />'
                                                        'Must only contain characters "a-zA-Z0-9_-".')
    name = models.CharField(max_length=128)
    public = models.BooleanField(default=True)
    users_group = models.ForeignKey(Group, blank=True, null=True, related_name='users_of_competition')
    administrators_group = models.ForeignKey(Group, blank=True, null=True, related_name='administrators_of_competition')
    contests = SortedManyToManyField(Contest)

    class Meta:
        verbose_name = _('competition')
        verbose_name_plural = _('competitions')

    def is_visible_for_user(self, user):
        return (
            self.public or
            user.is_superuser or
            user.is_staff or
            self.users_group in user.groups.all()
        )

    def get_visible_contests(self, user):
        if user.is_staff:
            return self.contests.all()
        else:
            return self.contests.filter(visible=True)

    def __str__(self):
        return u'{} ({})'.format(self.name, self.slug)
