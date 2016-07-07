import os

from django.conf import settings
from django.http import Http404
from django.template.loader import render_to_string
from sendfile import sendfile


class StatementsBackend(object):
    def render_statement(self, request, task):
        return ''

    def download_statement(self, request, task):
        raise Http404


class StatementsPDFBackend(StatementsBackend):
    def statement_path(self, task):
        return os.path.join(settings.TASK_STATEMENTS_PATH, task.contest.slug, task.slug, task.slug + '.pdf')

    def has_statement(self, task):
        return os.path.exists(self.statement_path(task))

    def render_statement(self, request, task):
        return render_to_string(
            template_name='tasks/parts/download_statement_button.html',
            context={'task': task, 'has_statement': self.has_statement(task)},
            request=request,
        )

    def download_statement(self, request, task):
        if self.has_statement(task):
            response = sendfile(
                request,
                self.statement_path(task),
            )
            response['Content-Disposition'] = 'inline; filename="{}"'.format(task.slug + '.pdf')
            return response
        else:
            raise Http404
