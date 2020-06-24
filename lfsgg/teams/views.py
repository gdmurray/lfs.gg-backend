from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from lfsgg.scrims.serializers import CondensedScrimSerializer
from lfsgg.scrims.models import Scrim

from .utils import get_team
from .models import Team
from .serializers import TeamViewSerializer
from .permissions import user_belongs_to_team


# Create your views here.

class TeamPublicInfoView(APIView):
    def get(self, request, identifier, *args, **kwargs):
        try:
            team = get_team(identifier)
        except Team.DoesNotExist:
            return Response(status=404)

        serializer = TeamViewSerializer(team, many=False)
        return Response(status=200, data=serializer.data)
