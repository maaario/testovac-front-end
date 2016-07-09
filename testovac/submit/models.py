import os

from django.conf import settings as django_settings
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _


from . import settings as submit_settings
from . import constants


class SubmitConfig(models.Model):
    """
    This is an abstract model providing JSONField to store submit configurations.
    """
    configuration = JSONField(default=dict)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class SubmitReceiverTemplate(SubmitConfig):
    """
    When creating a new submit receiver user can choose a template.
    """
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'submit receiver template'
        verbose_name_plural = 'submit receiver templates'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class SubmitReceiver(SubmitConfig):
    """
    Submit receiver manages one type of submits belonging to 1 Submit Receiver Group.
    """
    class Meta:
        verbose_name = 'submit receiver'
        verbose_name_plural = 'submit receivers'

    def __str__(self):
        return import_string(submit_settings.SUBMIT_DISPLAY_SUBMIT_RECEIVER_NAME)(self)


@python_2_unicode_compatible
class Submit(models.Model):
    """
    Submit holds information about user-submitted data.
    """
    receiver = models.ForeignKey(SubmitReceiver)
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL)
    time = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=128, blank=True)

    NOT_ACCEPTED = 0
    ACCEPTED_WITH_PENALIZATION = 1
    ACCEPTED = 2
    IS_ACCEPTED_CHOICES = [
        (NOT_ACCEPTED, _('no')),
        (ACCEPTED_WITH_PENALIZATION, _('with penalization')),
        (ACCEPTED, _('yes')),
    ]
    is_accepted = models.IntegerField(default=ACCEPTED, choices=IS_ACCEPTED_CHOICES)

    def dir_path(self):
        return os.path.join(submit_settings.SUBMIT_PATH, 'submits',
                            str(self.user.id), str(self.receiver.id), str(self.id))

    def file_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.SUBMITTED_FILE_EXTENSION)

    def file_exists(self):
        return os.path.exists(self.file_path())

    def last_review(self):
        reviews = self.review_set.order_by('-time')
        if reviews:
            return reviews[0]
        return None

    def get_absolute_url(self):
        return reverse('testovac.submit.views.view_submit', kwargs=dict(submit_id=self.id))

    class Meta:
        verbose_name = 'submit'
        verbose_name_plural = 'submits'

    def __str__(self):
        return '%s - <%s> (%s)' % (
            self.user,
            self.receiver,
            self.time.strftime('%H:%M:%S %d.%m.%Y'),
        )


@python_2_unicode_compatible
class Review(models.Model):
    """
    Holds information about feedback for one submit. This feedback can be created manually or automatically.
    """
    submit = models.ForeignKey(Submit)
    score = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    short_response = models.CharField(max_length=128, blank=True)
    comment = models.TextField(blank=True)
    filename = models.CharField(max_length=128, blank=True)

    def display_score(self):
        return import_string(submit_settings.SUBMIT_DISPLAY_SCORE)(self)

    def verbose_response(self):
        return constants.ReviewResponse.verbose(self.short_response)

    def file_path(self):
        return os.path.join(self.submit.dir_path(), str(self.id) + constants.REVIEWED_FILE_EXTENSION)

    def file_exists(self):
        return os.path.exists(self.file_path())

    def raw_path(self):
        return os.path.join(self.submit.dir_path(), str(self.id) + constants.TESTING_RAW_EXTENSION)

    def protocol_path(self):
        return os.path.join(self.submit.dir_path(), str(self.id) + constants.TESTING_PROTOCOL_EXTENSION)

    def protocol_exists(self):
        return os.path.exists(self.protocol_path())

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return 'review %d for submit %s' % (self.id, str(self.submit))
