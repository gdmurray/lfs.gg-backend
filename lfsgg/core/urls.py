from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^api/echo/$', EchoView.as_view()),
    url(r'^api/user/$', UserDataView.as_view())
]
