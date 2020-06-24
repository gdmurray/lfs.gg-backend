from django.db import models
from django.conf import settings
from lfsgg.constants import Region, TIMEZONES, ManagementStatus, ManagementRole, Platform
from lfsgg.utils import caps_fmt
from lfsgg.scrims.models import Schedule
from django.db.models.signals import post_save
from django.dispatch import receiver
from lfsgg.core.models import Game
import uuid


# Create your models here.
class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=60, null=False)
    logo = models.FileField(null=True, blank=True)

    game = models.ForeignKey('core.Game', null=False, default=Game.default_game, on_delete=models.DO_NOTHING)
    esl_link = models.URLField(max_length=200, null=True, blank=True)
    # Whether lfs or a user created it

    leagues = models.ManyToManyField('leagues.League', related_name='leagues', through='leagues.TeamLeague')

    slug = models.CharField(max_length=32, null=True, blank=True, unique=True)
    user_created = models.BooleanField(default=False)
    created_by = models.ForeignKey('core.User', null=True, on_delete=models.DO_NOTHING, blank=True)

    approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamSettings(models.Model):
    VIEW_PUBLIC = "PUBLIC"  # Anybody, even if not logged in IGNORES BLACKLIST
    VIEW_ANYONE = "ANYONE"  # Anybody who is logged in, except blacklist
    VIEW_LEAGUE_LISTS = "LEAGUE+LISTS"  # Anybody in your open_to leagues + whitelist - blacklist
    VIEW_LISTS = "LISTS"  # anybody in your whitelist + blacklist
    VIEW_PRIVATE = "PRIVATE"  # Nobody
    VIEW_PRIVACY_CHOICES = (
        (VIEW_PUBLIC, "Public"),
        (VIEW_ANYONE, "Anyone"),
        (VIEW_LEAGUE_LISTS, "Leagues and Whitelist"),
        (VIEW_LISTS, "Whitelist"),
        (VIEW_PRIVATE, "Private")
    )
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=False)

    region = models.CharField(choices=Region.CHOICES, max_length=10, null=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, null=True, blank=True)
    platform = models.CharField(choices=Platform.CHOICES, default=Platform.PC, max_length=15, null=False, blank=False)

    has_pro = models.BooleanField(default=False)
    esl_sync_enabled = models.BooleanField(default=False)

    # Team Listings
    whitelist = models.ManyToManyField(Team, related_name='whitelist', blank=True)
    blacklist = models.ManyToManyField(Team, related_name='blacklist', blank=True)

    # todo: Sync League with Open_To on default
    open_to = models.ManyToManyField('leagues.League', related_name='open_to', blank=True)

    # What leagues the team belongs to

    # Privacy Settings
    view_scrims_privacy = models.CharField(max_length=20, choices=VIEW_PRIVACY_CHOICES, default=VIEW_LEAGUE_LISTS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_timezone(self):
        if not self.timezone:
            return settings.DEFAULT_TZ
        return self.timezone

    # TODO: NEED TO WRITE TEST CASES FOR THIS
    def team_can_view(self, team=None) -> bool:
        if self.view_scrims_privacy == self.VIEW_PUBLIC:
            return True
        if self.view_scrims_privacy == self.VIEW_PRIVATE:
            return False

        if team:
            if team in self.blacklist.all():
                return False

            if self.view_scrims_privacy == self.VIEW_ANYONE:
                return True

            if self.view_scrims_privacy in [self.VIEW_LEAGUE_LISTS, self.VIEW_LISTS]:
                if team in self.whitelist.all():
                    return True

                if self.view_scrims_privacy == self.VIEW_LEAGUE_LISTS:
                    team_leagues_set = set([l.id for l in team.leagues.all()])
                    self_open_set = set([l.id for l in self.open_to.all()])
                    if len(self_open_set.intersection(team_leagues_set)) > 0:
                        return True
        return False


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
