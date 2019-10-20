from django.contrib import admin
from .models import Team, TeamManagement


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    class Meta:
        model = Team
