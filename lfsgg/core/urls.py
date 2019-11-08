from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *
from lfsgg.mail import AWSBounceHandler, AWSComplaintHandler
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^api/echo/$', EchoView.as_view()),
    url(r'^api/user/$', UserDataView.as_view()),
    url(r'^api/user/register/$', RegisterView.as_view(), name='register-user'),

    # Internal System Views
    url(r'^a/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    url(r'^a/password_reset/$', auth_views.PasswordResetView, name='password_reset'),

    # Testing
    url(r'^test/', test_template, name='test-template'),
    url(r'^send_email/', test_email_send, name='test-email-send'),

    # AWS Handling
    url(r'^aws/sns/handle-bounces', AWSBounceHandler.as_view(), name='aws-sns-handle-bounces'),
    url(r'^aws/sns/handle-complaints', AWSComplaintHandler.as_view(), name='aws-sns-handle-complaints')

]
