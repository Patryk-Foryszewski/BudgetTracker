from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Budget, Expense, Income

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


# class Album(models.Model):
#     album_name = models.CharField(max_length=100)
#     artist = models.CharField(max_length=100)
#
# class Track(models.Model):
#     album = models.ForeignKey(Album, related_name='tracks')
#     order = models.IntegerField()
#     title = models.CharField(max_length=100)
#     duration = models.IntegerField()
#
#     class Meta:
#         unique_together = ('album', 'order')
#         order_by = 'order'
#
#     def __unicode__(self):
#         return '%d: %s' % (self.order, self.title)
#
# class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ('order', 'title')
#
# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = TrackSerializer(many=True)
#
#     class Meta:
#         model = Album
#         fields = ('album_name', 'artist', 'tracks')


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ("pk", "name", "value", "created_date", "modified_date", "creator")


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("pk", "name", "value", "created_date", "modified_date", "creator")


class BudgetDetailSerializer(serializers.ModelSerializer):
    income = IncomeSerializer(many=True)
    expenses = ExpenseSerializer(many=True)

    class Meta:
        model = Budget
        fields = (
            "name",
            "created_date",
            "modified_date",
            "creator",
            "participants",
            "income",
            "expenses",
        )
