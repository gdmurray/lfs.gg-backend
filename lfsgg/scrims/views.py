from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .models import Schedule, Scrim
from .serializers import ScheduleTwitterSerializer
from lfsgg.teams.models import Team


# Create your views here.
def scrim_schedule_uuid(request, uuid):
    try:
        schedule = Schedule.objects.get(id=uuid)
    except Schedule.DoesNotExist:
        return Http404

    if "Twitterbot" in request.headers.get("User-Agent"):
        print("From Twitter Scraping Bot")
        serializer = ScheduleTwitterSerializer(schedule, many=False).data
        return render(request, 'twitter_schedule.html', context=serializer)
    else:
        return HttpResponseRedirect(f"https://r6pl.com/team/{uuid}")
        # TODO: Error Handling
    # TODO: Add Logic in which


def scrim_schedule_slug(request, slug):
    pass


def generate_scrim_image(request, team):
    pass
