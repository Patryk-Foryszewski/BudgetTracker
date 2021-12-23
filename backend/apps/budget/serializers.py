from rest_framework import serializers
from django.conf import settings

from .models import Budget

User = settings.AUTH_USER_MODEL


class BudgetCreateSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ["name", "content", "creator"]
