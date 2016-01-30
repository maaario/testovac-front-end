from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import Group

from datetime import datetime


@python_2_unicode_compatible
class Competition(models.Model):
    """
    Independent competition, consists of contests.
    Competition can be made accessible only to specific group of users.
    """
    name = models.CharField(max_length=128)
    public = models.BooleanField(default=True)
    users_group = models.ForeignKey(Group, blank=True, null=True)

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

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Contest(models.Model):
    """
    One round or competition event, consists of tasks.
    Holds information about deadline and visibility.
    """
    name = models.CharField(max_length=128)
    competition = models.ForeignKey(Competition)
    number = models.IntegerField()
    start_time = models.DateTimeField(default=datetime.now().replace(minute=0, second=0, microsecond=0))
    end_time = models.DateTimeField(default=datetime.now().replace(minute=0, second=0, microsecond=0))
    visible = models.BooleanField(default=False)

    def is_visible_for_user(self, user):
        return (
            user.is_superuser or
            user.is_staff or
            (self.visible and datetime.now() > self.start_time and self.competition.is_visible_for_user(user))
        )

    class Meta:
        verbose_name = _('contest')
        verbose_name_plural = _('contests')

    def __str__(self):
        return '%i. %s, %s' % (self.number, self.name, self.competition)


@python_2_unicode_compatible
class Task(models.Model):
    """
    General task data not related to testing are defined here.
    """
    name = models.CharField(max_length=128)
    contest = models.ForeignKey(Contest)
    number = models.IntegerField()
    max_points = models.IntegerField()

    def is_visible_for_user(self, user):
        return self.contest.is_visible_for_user(user)

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return self.name
