from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

urlpatterns = [
    path('s/<slug:slug>', scrim_schedule_image),
    path('api/scrims/<int:scrim_id>', ScrimView.as_view()),
    path('api/scrims/', CreateScrimView.as_view()),
    # Self Team Functions
    path('api/team/<slug:identifier>/calendar/scrims', TeamScrimsCalendarView.as_view()),
    path('api/team/<slug:identifier>/scrims/', TeamScrimsListView.as_view()),

    # External Team Functions
    path('api/team/<slug:identifier>/view/scrims', ExternalTeamScrimsView.as_view()),

]
