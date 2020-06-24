from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

urlpatterns = [
    path('api/team/<slug:identifier>/view', TeamPublicInfoView.as_view())
]
