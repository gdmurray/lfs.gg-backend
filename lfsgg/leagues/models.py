from django.db import models
from lfsgg.constants import ManagementStatus, ManagementRole


class LeagueRequest(models.Model):
    """
    An object that contains the request for league creation
    """
    APPLIED = "APPLIED"
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    STATUS_CHOICES = (
        (APPLIED, "Applied"),
        (APPROVED, "Approved"),
        (DECLINED, "Declined")
    )

    league = models.ForeignKey('leagues.League', on_delete=models.CASCADE)

    status = models.CharField(choices=STATUS_CHOICES, max_length=15, default=APPLIED)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('core.User', related_name='league_approved_by', null=True,
                                    on_delete=models.DO_NOTHING, blank=True)
    approved_on = models.DateTimeField(null=True)
    approved_notes = models.TextField(max_length=1000, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class League(models.Model):
    name = models.CharField(max_length=60, null=False)
    logo = models.FileField(null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True)
    official = models.BooleanField(default=False)

    open = models.BooleanField(default=True)

    user_created = models.BooleanField(default=True)
    created_by = models.ForeignKey('core.User', null=True, on_delete=models.DO_NOTHING, blank=True)

    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LeagueSettings(models.Model):
    pass


class TeamLeague(models.Model):
    """
    M2M Through Table connecting Teams to Leagues,
    """
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('core.User', related_name='league_user_approved_by', null=True,
                                    on_delete=models.DO_NOTHING, blank=True)
    approved_on = models.DateTimeField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class LeagueManagement(models.Model):
    """
    M2M Through Table connecting Owners/Users to a League
    """
    user = models.ForeignKey('core.User', related_name='league_user', on_delete=models.DO_NOTHING)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    role = models.CharField(choices=ManagementRole.CHOICES, default=ManagementRole.USER, max_length=10)

    status = models.CharField(choices=ManagementStatus.CHOICES, default=ManagementStatus.APPLIED, max_length=12)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('core.User', related_name='approved_by', null=True, on_delete=models.DO_NOTHING,
                                    blank=True)
    approved_on = models.DateTimeField(null=True, blank=True)
    approved_notes = models.TextField(max_length=1000, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
