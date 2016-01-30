from django.conf.urls import include, url
from django.contrib import admin

import testovac.tasks.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include(testovac.tasks.urls)),
]
