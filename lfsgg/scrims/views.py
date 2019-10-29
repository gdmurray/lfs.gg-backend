from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Schedule, Scrim
from .serializers import *
from lfsgg.teams.models import Team
from lfsgg.teams.utils import get_team
from lfsgg.utils import is_uuid_v1

from django.db.models import Q


def scrim_schedule_image(request, identifier):
    team, schedule = None, None
    if is_uuid_v1(identifier):
        try:
            schedule = Schedule.objects.get(id=identifier)
        except Schedule.DoesNotExist:
            return Http404
    else:
        try:
            team = Team.objects.get(slug=identifier)
        except Team.DoesNotExist:
            return Http404
        else:
            if not team.teamsettings.has_pro:
                return HttpResponse(status=403)

    if team:
        schedule = Schedule.objects.get(team=team, constant=True)

    if "Twitterbot" in request.headers.get("User-Agent"):
        serializer = ScheduleTwitterSerializer(schedule, many=False).data
        return render(request, 'twitter_schedule.html', context=serializer)
    else:
        return HttpResponseRedirect(f"https://r6pl.com/team/{identifier}")


class ScrimView(APIView):
    def get(self, request, scrim_id, *args, **kwargs):
        pass

    def put(self, request, scrim_id, *args, **kwargs):
        pass


class CreateScrimView(APIView):
    def post(self, request, *args, **kwargs):
        pass


class TeamScrimsCalendarView(APIView):
    """
    Only for Owners, Managers, Players of a Team
    Shows scrims that they are doing.
    """

    def get(self, request, identifier, *args, **kwargs):
        try:
            team = get_team(identifier)
        except Team.DoesNotExist:
            return Response(status=404)

        scrims = Scrim.objects.filter(
            Q(origin_team=team) | Q(secondary_team=team, status__in=[Scrim.CONFIRMED, Scrim.CANCELLED])
        )
        serializer = ScrimCalendarSerializer(scrims, many=True).data
        return Response(serializer, status=200)
