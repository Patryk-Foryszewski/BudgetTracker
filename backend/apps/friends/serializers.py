from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Friends

User = get_user_model()


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
