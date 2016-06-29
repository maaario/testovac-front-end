from django.conf.urls import url

from .views import post_submit, view_submit

urlpatterns = [
    url(r'post/(?P<receiver_id>\d+)/$', post_submit, name='post_submit'),
    url(r'view/(?P<submit_id>\d+)/$', view_submit, name='view_submit'),
]
