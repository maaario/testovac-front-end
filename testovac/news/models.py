from markdown import markdown

from django.db import models
from django.utils.html import mark_safe
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from testovac.tasks.models import Competition


@python_2_unicode_compatible
class Entry(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='news_entries')
    pub_date = models.DateTimeField(verbose_name='publication date', auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField(help_text='Content will be interpreted via <a '
                            'href="http://en.wikipedia.org/wiki/Markdown">'
                            'Markdown</a>.')
    competitions = models.ManyToManyField(Competition)

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)
        verbose_name = _('announcement')
        verbose_name_plural = _('announcements')

    def __str__(self):
        return self.title

    def rendered_text(self):
        return mark_safe(markdown(self.text, safe_mode=False))
