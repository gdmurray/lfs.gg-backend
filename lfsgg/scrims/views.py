from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Schedule, Scrim
from .serializers import *
from lfsgg.teams.models import Team
from lfsgg.teams.utils import get_team
from lfsgg.teams.permissions import user_belongs_to_team
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
        try:
            scrim = Scrim.objects.get(uuid=scrim_id)
        except Scrim.DoesNotExist:
            return Response(status=404)

        # serializer =

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


class TeamScrimsListView(APIView):
    def get(self, request, identifier, *args, **kwargs):
        try:
            team = get_team(identifier)
        except Team.DoesNotExist:
            return Response(status=404)

        if not user_belongs_to_team(request.user, team):
            return Response(status=403)

        scrims = Scrim.objects.filter(Q(origin_team=team) | Q(secondary_team=team),
                                      status__in=[Scrim.CONFIRMED, Scrim.CANCELLED, Scrim.LOOKING])
        serializer = CondensedScrimSerializer(scrims, many=True).data
        return Response(serializer, status=200)


class ExternalTeamScrimsView(APIView):
    """
    Function to return the scrims on the front page of a team from a different viewer
    """

    def get(self, request, identifier, *args, **kwargs):
        try:
            team = get_team(identifier)
        except Team.DoesNotExist:
            return Response(status=404)

        # Vars passed, team1, viewer_team, request -> we want a bool, but also a func throw?
        # this function could work for now
        # todo: make this modular
        viewer_identifier = request.GET.get('viewer', None)
        if viewer_identifier:
            try:
                viewer_team = get_team(viewer_identifier)
            except Team.DoesNotExist:
                return Response(status=404)

            if not user_belongs_to_team(request.user, viewer_team):
                return Response(status=403)
        else:
            viewer_team = viewer_identifier

        if team.teamsettings.team_can_view(viewer_team):
            # todo: eventually add date enforcement
            scrims = Scrim.objects.filter(origin_team=team, status=Scrim.LOOKING)
            serializer = CondensedScrimSerializer(scrims, many=True)
            return Response(status=200, data=serializer.data)
        else:
            return Response(status=403)
