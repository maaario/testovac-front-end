from django.conf.urls import url
from django.contrib.auth.views import logout

from testovac.login.views import login, register

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='registration'),
]
