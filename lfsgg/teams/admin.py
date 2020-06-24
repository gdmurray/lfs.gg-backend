from django.contrib import admin
from .models import Team, TeamManagement, TeamSettings
from lfsgg.leagues.models import TeamLeague
from logging import getLogger

logger = getLogger(__name__)


class TeamManagementInline(admin.StackedInline):
    extra = 0
    model = TeamManagement
    fields = ('user', 'role', 'status', 'approved', 'approved_by', 'approved_notes', 'created', 'updated')
    readonly_fields = ('created', 'updated', 'approved_by')


class TeamLeagueInline(admin.TabularInline):
    extra = 0
    model = TeamLeague
    fields = ('team', 'league', 'approved', 'approved_by', 'approved_on')
    readonly_fields = ('approved_on',)


class TeamSettingsInline(admin.StackedInline):
    extra = 0
    model = TeamSettings
    fieldsets = (
        (None, {
            'fields': ('region', 'timezone', 'has_pro', 'esl_sync_enabled', 'created', 'updated')
        }),
        ('Other Team Settings', {
            'fields': ('whitelist', 'blacklist')
        }),
        ('League Settings', {
            'fields': ('open_to',)
        })
    )
    readonly_fields = ('created', 'updated')
    verbose_name_plural = 'Team Settings'
    verbose_name = 'Team Settings'


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'game')
    readonly_fields = ('id', 'created', 'updated', 'created_by')
    inlines = (TeamSettingsInline, TeamManagementInline, TeamLeagueInline)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        def set_user(instance):
            print("instance, ", instance)
            print("approved by", instance.approved_by)

            if not instance.approved_by:
                print("Setting Approved_by to", request.user)
                instance.approved_by = request.user
                instance.save()

        if formset.model == TeamManagement:
            print("MODEL TEAM")
            instances = formset.save(commit=False)
            print(len(instances))
            for inst in instances:
                print("Setting inst")
                set_user(inst)
            formset.save_m2m()
            return instances
        else:
            return formset.save()

    class Meta:
        model = Team


admin.site.register(Team, TeamAdmin)
