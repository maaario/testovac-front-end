from django.db import models
from django.conf import settings as django_settings
from django.utils.encoding import python_2_unicode_compatible

import os

from . import settings as submit_settings
from . import constants


@python_2_unicode_compatible
class SubmitReceiver(models.Model):
    """
    Submit receiver manages different types of submits belonging to 1 object, e.g. task.
    """
    has_source = models.BooleanField()
    has_description = models.BooleanField()
    has_testable_zip = models.BooleanField()
    has_external = models.BooleanField()

    source_points = models.IntegerField(default=0)
    description_points = models.IntegerField(default=0)
    testable_zip_points = models.IntegerField(default=0)
    external_points = models.IntegerField(default=0)

    external_submit_link = models.CharField(max_length=128, blank=True, null=True)

    def has_submit_type(self, submit_type):
        check_field = {
            Submit.SOURCE: self.has_source,
            Submit.DESCRIPTION: self.has_description,
            Submit.TESTABLE_ZIP: self.has_testablezip,
            Submit.EXTERNAL: self.has_testable_zip,
        }
        return check_field[submit_type]

    class Meta:
        verbose_name = 'submit receiver'
        verbose_name_plural = 'submit receivers'

    def __str__(self):
        return str(self.id)


@python_2_unicode_compatible
class Submit(models.Model):
    """
    Submit holds information about its receiver and person who submitted it.
    There are 3 files that belong to each tested submit:
     source - file submitted by user
     raw - description file for tester
     protocol - results of testing
    """
    receiver = models.ForeignKey(SubmitReceiver)
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL)
    time = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=128, blank=True)

    SOURCE = 0
    DESCRIPTION = 1
    TESTABLE_ZIP = 2
    EXTERNAL = 3
    SUBMIT_TYPES = [
        (SOURCE, 'source'),
        (DESCRIPTION, 'description'),
        (TESTABLE_ZIP, 'testable_zip'),
        (EXTERNAL, 'external'),
    ]
    type = models.IntegerField(choices=SUBMIT_TYPES)

    points = models.DecimalField(max_digits=5, decimal_places=2)
    manually_approved = models.BooleanField()

    testing_finished = models.BooleanField(blank=True)
    tester_response = models.CharField(max_length=10, blank=True)

    reviewed = models.BooleanField(blank=True)
    reviewer_comment = models.TextField(blank=True)

    def dir_path(self):
        return os.path.join(submit_settings.SUBMIT_PATH, 'submits', self.user.id, self.receiver.id)

    def source_path(self):
        return self.dir_path() + str(self.id) + constants.SUBMIT_SOURCE_FILE_EXTENSION

    def protocol_path(self):
        return self.dir_path() + str(self.id) + constants.SUBMIT_PROTOCOL_FILE_EXTENSION

    def raw_path(self):
        return self.dir_path() + str(self.id) + constants.SUBMIT_RAW_FILE_EXTENSION

    class Meta:
        verbose_name = 'submit'
        verbose_name_plural = 'submits'

    def __str__(self):
        return '%s - %s <%s> (%s)' % (
            self.user,
            self.receiver,
            self.get_type_display(),
            str(self.time),
        )
