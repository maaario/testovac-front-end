from django.conf.urls import url

from testovac.tasks.views import contest_list, task_statement

urlpatterns = [
    url(r'^$', contest_list, name='contest_list'),
    url(r'^(?P<task_id>\d+)/$', task_statement, name='task_statement'),
]
