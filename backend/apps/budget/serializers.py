from rest_framework import serializers
from . models import Budget


from django.conf import settings

User = settings.AUTH_USER_MODEL


class BudgetCreateSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ['name', 'content', 'creator']


class UserListingField(serializers.RelatedField):
    def to_representation(self, user):
        return user.username


class BudgetListSerializer(serializers.ModelSerializer):
    creator = UserListingField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ['name', 'creator', 'creator']


class BudgetSerializer(serializers.ModelSerializer):
    """Book serializer for all fields."""

    class Meta:
        model = Budget
        fields = '__all__'
