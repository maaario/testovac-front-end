from django.conf.urls import url
from django.utils.module_loading import import_string

from . import settings as submit_settings
from .views import view_submit, receive_protocol, download_submit, download_review, get_receiver_templates
from .commands import rejudge_submit, rejudge_receiver_submits

urlpatterns = [
    url(r'^post/(?P<receiver_id>\d+)/$',
        import_string(submit_settings.SUBMIT_POST_SUBMIT_FORM_VIEW).as_view(),
        name='post_submit'),
    url(r'^view/(?P<submit_id>\d+)/$', view_submit, name='view_submit'),
    url(r'^download/submit/(?P<submit_id>\d+)/$', download_submit, name='download_submit'),
    url(r'^download/review/(?P<review_id>\d+)/$', download_review, name='download_review'),
    url(r'^receive_protocol/$', receive_protocol),

    url(r'^commands/rejudge/submit/(?P<submit_id>\d+)/$', rejudge_submit, name='rejudge_submit'),

    # This the url path for this command is currently deactivated.
    # Also the button at submit_list template is hidden to prevent misclicks that could cause a judge overflow.
    # TODO: Implement pop-up / confirmation page for resubmit approval
    #url(r'^commands/rejudge/receiver/(?P<receiver_id>\d+)/$', rejudge_receiver_submits, name='rejudge_receiver_submits'),

    url(r'^ajax/get_receiver_templates/', get_receiver_templates),
]
