from rest_framework import serializers
from .models import Schedule


class ScheduleTwitterSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        if not obj.thumbnail:
            return obj.generate_image()
        print(obj.thumbnail.url)
        return obj.thumbnail.url

    def get_team_name(self, obj):
        return obj.team.name

    class Meta:
        fields = ('id', 'thumbnail', 'thumbnail_updated', 'team_name')
        model = Schedule
