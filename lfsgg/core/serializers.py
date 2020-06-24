from rest_framework import serializers
from .models import User, Game
from lfsgg.teams.serializers import TeamManagementSerializer
from lfsgg.teams.models import TeamManagement


class UserDataSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()

    def get_teams(self, obj):
        teams = TeamManagement.objects.filter(user_id=obj.id, approved=True)
        if teams.count() > 0:
            return TeamManagementSerializer(teams, many=True).data
        return []

    class Meta:
        fields = ('username', 'email', 'active_team', 'teams', 'email_confirmed')
        model = User
        extra_kwargs = {
            'teams': {'read_only': True},
            'email_confirmed': {'read_only': True},
        }

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'logo', 'short_code')
        model = Game
