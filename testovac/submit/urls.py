from django.conf.urls import url

from .views import view_submit, post_submit

urlpatterns = [
    url(r'view/(?P<submit_id>\d+)/$', view_submit, name='view_submit'),
    url(r'post/(?P<receiver_id>\d+)/$', post_submit, name='post_submit'),

    # url(r'submit_page/(?P<receiver_id>\d+)/$', None, name='receiver_submit_page'),
    #
    # url(r'protocol/(?P<submit_id>\d+)/$', None, name='receive_protocol'),
    #
    # url(r'judge/now/$', None, name='judge_now'),
    # url(r'judge/mine/$', None, name='judge_mine'),
]
