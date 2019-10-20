from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    player = models.ForeignKey('teams.Player', null=True, on_delete=models.DO_NOTHING)

    created = models.DateTimeField(auto_created=True)
    updated = models.DateTimeField(auto_now=True)