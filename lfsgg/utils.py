import pytz
from django.conf import settings
from uuid import UUID
import uuid


def caps_fmt(s):
    return s.lower().capitalize()


def inc(c, x=0, y=0):
    c = list(c)
    c[0] += x
    c[1] += y
    return tuple(c)


def to_team_tz(dt, team):
    timezone = team.teamsettings.timezone if team.teamsettings.timezone else settings.DEFAULT_TZ
    # print(timezone)
    return dt.astimezone(pytz.timezone(timezone))


def is_uuid_v1(identifier, version=1):
    try:
        uuid_obj = UUID(identifier, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == identifier
