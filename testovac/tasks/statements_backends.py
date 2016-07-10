import os
import glob

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
    def search_paths(self, task):
        return [
            os.path.join(settings.TASK_STATEMENTS_PATH, task.contest.slug, task.slug + '.pdf'),
            os.path.join(settings.TASK_STATEMENTS_PATH, task.contest.slug, task.slug + '-*.pdf'),
            os.path.join(settings.TASK_STATEMENTS_PATH, task.slug + '.pdf'),
            os.path.join(settings.TASK_STATEMENTS_PATH, task.slug + '-*.pdf'),
        ]

    def find_statement(self, task):
        for pattern in self.search_paths(task):
            matches = glob.glob(pattern)
            if len(matches) > 1:
                return False, 'More matches found for pattern {}'.format(pattern)
            if len(matches) == 1:
                return True, matches[0]
        return False, 'No statement found'

    def render_statement(self, request, task):
        has_statement, message = self.find_statement(task)
        return render_to_string(
            template_name='tasks/parts/download_statement_button.html',
            context={'task': task, 'has_statement': has_statement, 'message': message},
            request=request,
        )

    def download_statement(self, request, task):
        has_statement, path = self.find_statement(task)
        if has_statement:
            response = sendfile(
                request,
                path,
            )
            response['Content-Disposition'] = 'inline; filename="{}"'.format(task.slug + '.pdf')
            return response
        else:
            raise Http404
