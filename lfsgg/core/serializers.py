from rest_framework import serializers
from .models import User


class EchoSerializer(serializers.Serializer):
    message = serializers.CharField()


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User
