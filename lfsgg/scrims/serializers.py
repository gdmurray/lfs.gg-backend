from rest_framework import serializers
from .models import Schedule, Scrim
import datetime


class ScheduleTwitterSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        if not obj.thumbnail:
            return obj.generate_image()

        return obj.thumbnail.url

    def get_team_name(self, obj):
        return obj.team.name

    class Meta:
        fields = ('id', 'thumbnail', 'thumbnail_updated', 'team_name')
        model = Schedule


class CondensedScrimSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    def get_time(self, obj):
        return obj.get_time()

    class Meta:
        fields = ('id', 'uuid', 'secondary_team', 'status', 'request_notes', 'time')
        model = Scrim

class ScrimDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'uuid', 'status', 'origin_team', 'secondary_team', '')

class ScrimCalendarSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    textColor = serializers.SerializerMethodField()
    backgroundColor = serializers.SerializerMethodField()
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    allDay = serializers.SerializerMethodField()
    extendedProps = serializers.SerializerMethodField()

    def get_title(self, obj):
        if obj.status == Scrim.LOOKING:
            if obj.get_time().minute == 0:
                time = obj.get_time().strftime('%-I %p').lower()
            else:
                time = obj.get_time().strftime('%-I:%M %p').lower()
            return f"{time}: Looking"

    def get_textColor(self, obj):
        if obj.status == Scrim.LOOKING:
            return "black"

    def get_backgroundColor(self, obj):
        if obj.status == Scrim.LOOKING:
            return "yellow"

    def get_start(self, obj):
        return obj.get_time()

    def get_end(self, obj):
        return obj.get_time() + datetime.timedelta(hours=2)

    def get_allDay(self, obj):
        return 'false'

    def get_extendedProps(self, obj):
        return CondensedScrimSerializer(obj, many=False).data

    class Meta:
        model = Scrim
        fields = ('id', 'title', 'extendedProps', 'textColor', 'backgroundColor', 'start', 'end', 'allDay')

