from rest_framework import serializers

from django.conf import settings

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    registered_at = serializers.DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'avatar', 'username', 'registered_at']

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else settings.STATIC_URL + 'images/default_avatar.png'

    def get_username(self, obj):
        return obj.username

    class Meta:
        model = User
        fields = ['email', 'avatar', 'username', 'registered_at']


class UserListSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ['username', 'avatar']


class UserWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'username']
