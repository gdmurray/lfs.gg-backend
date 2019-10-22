from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

urlpatterns = [
    path('s/<uuid:uuid>', scrim_schedule_uuid),
    path('s/<slug:slug>', scrim_schedule_slug),
]
