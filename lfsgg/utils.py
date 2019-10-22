import pytz
from django.conf import settings


def caps_fmt(s):
    return s.lower().capitalize()


def inc(c, x=0, y=0):
    c = list(c)
    c[0] += x
    c[1] += y
    return tuple(c)


def to_team_tz(dt, team):
    timezone = team.teamsettings.timezone if team.teamsettings.timezone else settings.DEFAULT_TZ
    return dt.replace(tzinfo=pytz.timezone(timezone)).astimezone(pytz.timezone(timezone))
