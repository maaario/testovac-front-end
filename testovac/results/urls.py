from django.conf.urls import url

from testovac.results.views import contest_results, contest_group_results

urlpatterns = [
    url(r'^contest/(?P<contest_slug>[\w-]+)/$', contest_results, name='contest_results'),
    url(r'^group/(?P<group_slug>[\w-]+)/$', contest_group_results, name='contest_group_results'),
]
