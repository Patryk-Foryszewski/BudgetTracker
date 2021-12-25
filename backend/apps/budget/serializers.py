from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Budget

User = get_user_model()


class BudgetCreateSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ["name", "content", "creator"]


class UserListingField(serializers.RelatedField):
    def to_representation(self, user):
        return user.username


class BudgetListSerializer(serializers.ModelSerializer):
    creator = UserListingField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ["name", "creator"]


class BudgetSerializer(serializers.ModelSerializer):
    """Book serializer for all fields."""

    class Meta:
        model = Budget
        fields = "__all__"


class BudgetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["name", "value"]


class BudgetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["created_date", "modified_date", "creator", "participants"]
