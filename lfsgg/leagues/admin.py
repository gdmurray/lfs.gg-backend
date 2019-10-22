from django.contrib import admin
from .models import League, LeagueManagement, LeagueRequest


# Register your models here.

class LeagueAdmin(admin.ModelAdmin):
    fields = ('name', 'logo', 'url', 'official', 'user_created', 'created_by', 'active', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'official', 'active')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class LeagueInline(admin.StackedInline):

    pass


class LeagueRequestAdmin(admin.ModelAdmin):
    fields = ('league', 'status', 'approved', 'approved_by', 'approved_on', 'approved_notes', 'created', 'updated')
    readonly_fields = ('approved_by', 'approved_on', 'created', 'updated')

    def save_model(self, request, obj, form, change):
        print(request)
        print(obj)
        print(form)
        print(change)
        super().save_model(request, obj, form, change)


admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueRequest, LeagueRequestAdmin)
