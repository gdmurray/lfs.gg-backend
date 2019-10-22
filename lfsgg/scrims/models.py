import pytz
import base64

import uuid
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

from lfsgg.utils import to_team_tz
from lfsgg.storage_backends import ScrimStorage
from .create_image import create_image
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import pytz


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
                                       on_delete=models.DO_NOTHING, blank=True)

    created_by = models.ForeignKey('core.User', related_name='created_by', on_delete=models.DO_NOTHING, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=12)
    request_notes = models.CharField(max_length=30, null=True, blank=True)

    scrim_notes = models.TextField(max_length=2000, null=True, blank=True)

    time = models.DateTimeField(null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_time(self):
        return to_team_tz(self.time, self.origin_team)

    def __str__(self):
        return f"{self.origin_team.name}: {self.status} - {self.get_time().strftime('%m/%d %H:%M')}"

    # todo write function to automatically close scrims 1 day later


class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    team = models.ForeignKey('teams.Team', related_name='schedule_team', on_delete=models.CASCADE)
    constant = models.BooleanField(default=True)
    scrims = models.ManyToManyField(Scrim, related_name='schedule_scrims')

    thumbnail = models.ImageField(storage=ScrimStorage(), blank=True)
    thumbnail_updated = models.DateTimeField(null=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def generate_image(self):
        self.thumbnail_updated = datetime.datetime.now(tz=pytz.timezone(self.team.teamsettings.get_timezone()))
        file, filename = create_image(self)
        self.thumbnail.save(filename, file)
        self.save()
        return self.thumbnail.url

    # todo: add expiry to non constant schedule
    def get_available_scrims(self):
        image_generated = False
        if self.constant:
            previous_scrims = {s.id: s for s in self.scrims.all()}
            previous_scrim_ids = set(previous_scrims.keys())
            # print("Previous Scrim ids: ", previous_scrim_ids)
            scrims = Scrim.objects.filter(origin_team=self.team, status=Scrim.LOOKING)[:15]

            current_scrims = {s.id: s for s in scrims}
            current_scrim_ids = {s.id for s in scrims}
            # print("Updated Scrim ids: ", current_scrim_ids)
            added = current_scrim_ids.difference(previous_scrim_ids)
            deleted = previous_scrim_ids.difference(current_scrim_ids)
            # print("Added: ", added)
            # print("Deleted: ", deleted)

            if len(added) > 0:
                for a in added:
                    self.scrims.add(current_scrims[a])

            if len(deleted) > 0:
                for d in deleted:
                    self.scrims.remove(previous_scrims[d])

            self.save()
            if len(added) > 0 or len(deleted) > 0:
                self.generate_image()
                image_generated = True
        else:
            if not self.thumbnail and len(self.scrims.all()) > 0:
                self.generate_image()
                image_generated = True

        return self.scrims, image_generated


@receiver(post_save, sender=Schedule)
def schedule_created(sender, instance, created, *args, **kwargs):
    if created:
        instance.get_available_scrims()

    if len(instance.scrims.all()) > 0 and not instance.thumbnail:
        instance.generate_image()


@receiver(post_save, sender=Scrim)
def scrim_updated(sender, instance, created, *args, **kwargs):
    # TODO: Find a way to see if any data has changed
    schedule = Schedule.objects.filter(team=instance.origin_team, constant=True).first()
    scrims, gen = schedule.get_available_scrims()
    if instance in scrims.all() and not gen:
        schedule.generate_image()

    schedules = Schedule.objects.filter(team=instance.origin_team, constant=False)

    for s in schedules:
        if instance in s.scrims.all():
            print("FOUND AFFECTED SCHEDULE")
            s.generate_image()
