from django.db import models
from django.conf import settings
from lfsgg.constants import Region, TIMEZONES, ManagementStatus, ManagementRole
from lfsgg.utils import caps_fmt
from lfsgg.scrims.models import Schedule
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=60, null=False)
    logo = models.FileField(null=True, blank=True)
    esl_link = models.URLField(max_length=200, null=True, blank=True)
    # Whether lfs or a user created it
    user_created = models.BooleanField(default=False)
    created_by = models.ForeignKey('core.User', null=True, on_delete=models.DO_NOTHING, blank=True)

    approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamSettings(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=False)
    region = models.CharField(choices=Region.CHOICES, max_length=10, null=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, null=True, blank=True)

    has_pro = models.BooleanField(default=False)
    esl_sync_enabled = models.BooleanField(default=False)
    open_to = models.ManyToManyField('leagues.League', related_name='open_to')
    leagues = models.ManyToManyField('leagues.League', related_name='leagues', through='leagues.TeamLeague')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_timezone(self):
        if not self.timezone:
            return settings.DEFAULT_TZ
        return self.timezone


@receiver(post_save, sender=Team)
def account_created(sender, instance, created, *args, **kwargs):
    if created:
        team_settings = TeamSettings.objects.create(team=instance)
        team_settings.save()

        schedule = Schedule.objects.create(team=instance, constant=True)
        schedule.save()


class TeamManagement(models.Model):
    """
    M2M Through Table connecting Owners/Users to a Team
    """
    user = models.ForeignKey('core.User', related_name='team_user', on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(choices=ManagementRole.CHOICES, default=ManagementRole.USER, max_length=10)

    status = models.CharField(choices=ManagementStatus.CHOICES, default=ManagementStatus.APPLIED, max_length=12)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('core.User', related_name='team_user_approved_by', null=True, blank=True,
                                    on_delete=models.DO_NOTHING)
    approved_on = models.DateTimeField(null=True)
    approved_notes = models.TextField(max_length=1000, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}, {caps_fmt(self.role)} of {self.team.name}: {caps_fmt(self.status)}"


class Player(models.Model):
    username = models.CharField(max_length=30, null=False)
    email = models.EmailField(null=True, max_length=64)

    p_id = models.CharField(max_length=64, null=True)
    p_user = models.CharField(max_length=64, null=True)

    current_mmr = models.IntegerField(null=True)
    current_rank = models.IntegerField(null=True)
    current_level = models.IntegerField(null=True)

    tab_banned = models.BooleanField(default=False)
    ban_reason = models.CharField(max_length=64, null=True)

    last_queried = models.DateTimeField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
