from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^api/echo/$', EchoView.as_view()),
    url(r'^api/user/$', UserDataView.as_view()),

    # Password Reset Views
    url(r'^a/password_reset/$', auth_views.PasswordResetView, name='password_reset'),

]
