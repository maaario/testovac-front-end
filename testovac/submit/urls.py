from django.conf.urls import url

from .views import post_submit

urlpatterns = [
    url(r'post/(?P<receiver_id>\d+)/$', post_submit, name='post_submit'),
]
