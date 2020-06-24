from rest_framework import serializers
from .models import TeamManagement, Team, TeamSettings


class BasicTeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'logo', 'game', 'active')
        model = Team


class TeamSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSettings
        fields = ('region', 'platform', 'timezone',)


class TeamViewSerializer(serializers.ModelSerializer):
    settings = serializers.SerializerMethodField()
    game = serializers.SerializerMethodField()

    def get_game(self, obj):
        from lfsgg.core.serializers import GameSerializer
        return GameSerializer(obj.game, many=False).data

    def get_settings(self, obj):
        return TeamSettingsSerializer(obj.teamsettings, many=False).data

    class Meta:
        model = Team
        fields = ('id', 'name', 'logo', 'game', 'settings')


class TeamManagementSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()

    def get_team(self, obj):
        return BasicTeamSerializer(obj.team, many=False).data

    class Meta:
        model = TeamManagement
        fields = ('team', 'role', 'status')
