import pytz

from django.db import models
from django.conf import settings

from lfsgg.utils import to_team_tz


class Scrim(models.Model):
    LOOKING = "LOOKING"
    CONFIRMED = "CONFIRMED"
    REQUESTED = "REQUESTED"
    DECLINED = "DECLINED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = (
        (LOOKING, "Looking"),
        (CONFIRMED, "Confirmed"),
        (REQUESTED, "Requested"),
        (DECLINED, "Declined"),
        (CANCELLED, "Cancelled")
    )

    origin_team = models.ForeignKey('teams.Team', related_name='origin_team', null=False, on_delete=models.CASCADE)
    secondary_team = models.ForeignKey('teams.Team', related_name='secondary_team', null=True,
                                       on_delete=models.DO_NOTHING)

    created_by = models.ForeignKey('core.User', related_name='created_by', on_delete=models.DO_NOTHING)
    status = models.CharField(choices=STATUS_CHOICES, max_length=12)
    request_notes = models.CharField(max_length=30, null=True)

    scrim_notes = models.TextField(max_length=2000, null=True)

    time = models.DateTimeField(null=False)

    created = models.DateTimeField(auto_created=True)
    updated = models.DateTimeField(auto_now=True)

    def get_time(self):
        return to_team_tz(self.time, self.origin_team)
