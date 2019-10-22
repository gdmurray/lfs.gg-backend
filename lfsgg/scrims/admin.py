from django.contrib import admin
from .models import Scrim, Schedule
from django.forms.models import BaseInlineFormSet
from django.urls import resolve
from logging import getLogger

logger = getLogger(__name__)


def create_schedule(modeladmin, request, queryset):
    # for testing purposes, assume first scrim is team
    if len(queryset) > 0:
        team = queryset[0].origin_team
        schedule = Schedule.objects.create(constant=False, team=team)
        for scrim in queryset:
            schedule.scrims.add(scrim)
        print(schedule.scrims)
        schedule.save()


create_schedule.short_description = 'Create Schedule For Selected Scrims'


class ScrimAdmin(admin.ModelAdmin):
    fields = (
        'origin_team', 'secondary_team', 'created_by', 'status', 'request_notes', 'scrim_notes', 'time', 'created',
        'updated')
    readonly_fields = ('created', 'updated')
    # filter_vertical = ('origin_team',)
    list_filter = ('origin_team',)
    actions = [create_schedule, ]
    list_display = ('origin_team', 'status', 'time', 'secondary_team')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ScrimInline(admin.TabularInline):
    # fields = ('status', 'origin_team', 'secondary_team', 'time', 'created_by', 'created', 'updated')
    # readonly_fields = ('created_by', 'created', 'updated')
    model = Schedule.scrims.through
    extra = 0
    verbose_name = 'Scrim'
    verbose_name_plural = 'Scrims'
    # formset = ScheduleScrimFormset


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('team', 'constant', 'thumbnail_updated', 'created')
    fields = ('id', 'team', 'constant', 'thumbnail', 'thumbnail_updated')
    readonly_fields = ('id', 'thumbnail_updated')
    inlines = (ScrimInline,)
    # filter_horizontal = ('constant',)


admin.site.register(Scrim, ScrimAdmin)
admin.site.register(Schedule, ScheduleAdmin)
