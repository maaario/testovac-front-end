from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

import testovac.tasks.urls
import testovac.news.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include(testovac.tasks.urls)),
    url(r'^news/', include(testovac.news.urls)),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
]
