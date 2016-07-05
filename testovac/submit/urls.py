from django.conf.urls import url

from .views import PostSubmitForm, view_submit, receive_protocol, download_submit, download_review, get_receiver_templates


urlpatterns = [
    url(r'^post/(?P<receiver_id>\d+)/$', PostSubmitForm.as_view(), name='post_submit'),
    url(r'^view/(?P<submit_id>\d+)/$', view_submit, name='view_submit'),
    url(r'^download/submit/(?P<submit_id>\d+)/$', download_submit, name='download_submit'),
    url(r'^download/review/(?P<review_id>\d+)/$', download_review, name='download_review'),
    url(r'^receive_protocol/$', receive_protocol),

    url(r'^ajax/get_receiver_templates/', get_receiver_templates),
]
