from django.conf.urls import url

from testovac.tasks.views import contest_list, task_statement, task_statement_download

urlpatterns = [
    url(r'^$', contest_list, name='contest_list'),
    url(r'^(?P<task_slug>[\w-]+)/$', task_statement, name='task_statement'),
    url(r'^(?P<task_slug>[\w-]+)/download/$', task_statement_download, name='task_statement_download'),
]
