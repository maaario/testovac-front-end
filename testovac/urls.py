from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.views.static import serve

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern
import news.urls

import testovac.login.urls
import testovac.tasks.urls
import testovac.submit.urls
import testovac.results.urls
from testovac.admin import admin_site_custom_index_view


def create_custom_admin_urls(urls):
    def get_admin_urls():
        return [
            url(r'^$', admin.site.admin_view(admin_site_custom_index_view))
        ] + urls
    return get_admin_urls

admin.site.get_urls = create_custom_admin_urls(admin.site.get_urls())


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include(testovac.tasks.urls)),
    url(r'^news/', include(news.urls)),
    url(r'^submit/', include(testovac.submit.urls)),
    url(r'^results/', include(testovac.results.urls)),
    url(r'^login/', include(testovac.login.urls)),
]

urlpatterns += [
    url(r'^notifications/', get_nyt_pattern()),
    url(r'^$', lambda r: HttpResponseRedirect('wiki/'), name='root'),
    url(r'^wiki/', get_wiki_pattern()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
