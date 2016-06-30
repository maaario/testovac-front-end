from django.conf.urls import url

from .views import PostSubmitForm, view_submit, receive_protocol


urlpatterns = [
    url(r'post/(?P<receiver_id>\d+)/$', PostSubmitForm.as_view(), name='post_submit'),
    url(r'view/(?P<submit_id>\d+)/$', view_submit, name='view_submit'),
    url(r'receive_protocol/$', receive_protocol),
]
