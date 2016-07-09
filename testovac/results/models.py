from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from testovac.tasks.models import Contest


@python_2_unicode_compatible
class CustomResultsTable(models.Model):
    slug = models.SlugField(primary_key=True,
                            help_text='Serves as part of URL.<br />'
                                      'Must only contain characters "a-zA-Z0-9_-".')
    name = models.CharField(max_length=128)
    contests = models.ManyToManyField(Contest)

    class Meta:
        verbose_name = _('custom results table')
        verbose_name_plural = _('custom results tables')

    def __str__(self):
        return u'{} ({})'.format(self.name, self.slug)
