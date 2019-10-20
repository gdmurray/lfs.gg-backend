import pytz
from django.conf import settings


def to_team_tz(dt, team):
    timezone = team.teamsettings.timezone if team.teamsettings.timezone else settings.DEFAULT_TZ
    return dt.replace(tzinfo=pytz.timezone(timezone)).astimezone(pytz.timezone(timezone))
