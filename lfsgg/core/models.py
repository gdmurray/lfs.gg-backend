from django.db import models
from django.contrib.auth.models import AbstractUser
from lfsgg.storage_backends import MediaStorage


# Create your models here.

class User(AbstractUser):
    player = models.ForeignKey('teams.Player', null=True, on_delete=models.DO_NOTHING)

    email_confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Game(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    short_code = models.CharField(max_length=5, null=False, blank=False)
    logo = models.ImageField(storage=MediaStorage(), blank=True, null=True)

    @staticmethod
    def default_game():
        dg = Game.objects.filter(short_code="R6S").first()
        if not dg:
            dg = Game(name="Rainbow Six Siege", short_code="R6S")
            dg.save()
        return dg.id

    def __str__(self):
        return self.name
