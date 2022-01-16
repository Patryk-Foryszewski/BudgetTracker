from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Friends

User = get_user_model()


class FriendsAddSerializer(serializers.ModelSerializer):
    """This id docstring of serializer"""

    class Meta:
        model = Friends
        fields = ["friends_list"]

    def update(self, instance, validated_data):
        instance.friends_list.add(*validated_data["friends_list"])
        instance.save()
        return instance


class FriendsRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ["friends_list"]

    def update(self, instance, validated_data):
        instance.friends_list.remove(*validated_data["friends_list"])
        instance.save()
        return instance


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "avatar"]
