from rest_framework import serializers
from django.db import transaction
from django.conf import settings

from apps.users.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer as DJ_Rest_Register_Serializer
from dj_rest_auth.serializers import LoginSerializer as DJ_Login_Serializer
from allauth.account import app_settings as allauth_settings


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


class RegisterSerializer(DJ_Rest_Register_Serializer):
    # overwrite "username" from dj_rest_auth field to get max_length from User model
    # and to be required for registration
    username = serializers.CharField(
        max_length=User._meta.get_field('username').max_length,
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=True,
    )

    @transaction.atomic
    def save(self, request):
        return super().save(request)


class LoginSerializer(DJ_Login_Serializer):
    # overwrite username field to None so it is not required to "Login"
    username = None
    email = serializers.EmailField(required=True, allow_blank=True)
