from django.conf.urls import url

from testovac.news.views import EntryListView


urlpatterns = [
    url(r'^$', EntryListView.as_view(), {'page': 1}, name='news'),
    url(r'^page/(?P<page>[0-9]+)/$', EntryListView.as_view(), name='news_page'),
]
