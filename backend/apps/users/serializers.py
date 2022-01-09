from allauth.account import app_settings as allauth_settings
from apps.users.models import Friends, User
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DJ_Rest_Register_Serializer,
)
from dj_rest_auth.serializers import LoginSerializer as DJ_Login_Serializer
from django.conf import settings
from django.db import transaction
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    registered_at = serializers.DateTimeField(format="%H:%M %d.%m.%Y", read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "avatar", "username", "registered_at"]

    def get_avatar(self, obj):
        return (
            obj.avatar.url
            if obj.avatar
            else settings.STATIC_URL + "images/default_avatar.png"
        )

    def get_username(self, obj):
        return obj.username


class UserListSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ["username", "avatar"]


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "username"]


class RegisterSerializer(DJ_Rest_Register_Serializer):
    # overwrite "username" from dj_rest_auth field to get max_length from User model
    # and to be required for registration
    username = serializers.CharField(
        max_length=User._meta.get_field("username").max_length,
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


class FriendsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ["friends_list"]

    def update(self, instance, validated_data):
        print("UPDATE", instance, validated_data)
        # instance.friends.bulk_update(validated_data['friends_list'], "friends_list")
        for friend in validated_data["friends_list"]:
            instance.friends_list.add(friend)
        return super().update(instance, validated_data)


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "avatar"]
