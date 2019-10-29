from lfsgg.utils import is_uuid_v1
from .models import Team


def get_team(identifier):
    if is_uuid_v1(identifier):
        team = Team.objects.get(id=identifier)
    else:
        team = Team.objects.get(slug=identifier)
    return team
