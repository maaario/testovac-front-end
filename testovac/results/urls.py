from django.conf.urls import url

from testovac.results.views import contest_results, custom_results

urlpatterns = [
    url(r'^contest/(?P<contest_slug>[\w-]+)/$', contest_results, name='contest_results'),
    url(r'^group/(?P<results_table_slug>[\w-]+)/$', custom_results, name='contest_group_results'),
]
