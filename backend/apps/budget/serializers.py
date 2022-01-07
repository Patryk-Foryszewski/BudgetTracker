from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q, Sum
from rest_framework import serializers

from .mixins import AddCreatorMixin, BudgetCreatorOrParticipantMixin, InstanceOrBudgetCreatorMixin
from .models import Budget, Expense, Income, Category

User = get_user_model()


class BudgetCreateSerializer(AddCreatorMixin, serializers.ModelSerializer):
    # creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ["name", "content"]


class UserListingField(serializers.RelatedField):
    def to_representation(self, user):
        return user.username


class BudgetListSerializer(serializers.ModelSerializer):
    creator = UserListingField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ["name", "creator"]


class BudgetUpdateSerializer(AddCreatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["name", "content", "participants"]

    def has_access(self, instance, validated_data):
        if validated_data["creator"] != instance.creator:
            raise PermissionDenied("Only Budget Creator can edit Budget")

    def update(self, instance, validated_data):
        self.has_access(instance, validated_data)
        return super().update(instance, validated_data)


class BudgetRemoveParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["participants"]

    def update(self, instance, validated_data):
        for participant in validated_data['participants']:
            instance.participants.remove(participant)
        instance.save()
        return instance


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = (
            "pk",
            "name",
            "budget",
            "value",
            "created_date",
            "modified_date",
            "creator",
        )


class ExpenseCreateSerializer(BudgetCreatorOrParticipantMixin, serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("name", "budget", "value", "category")


class ExpenseUpdateSerializer(InstanceOrBudgetCreatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("name", "value", "category")


class IncomeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ("name", "value")


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = (
            "pk",
            "name",
            "budget",
            "value",
            "created_date",
            "modified_date",
            "creator",
        )


class BudgetDetailSerializer(serializers.ModelSerializer):
    income = IncomeSerializer(many=True)
    expenses = ExpenseSerializer(many=True)
    expenses_sum = serializers.SerializerMethodField()
    budget_left = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = (
            "pk",
            "name",
            "created_date",
            "modified_date",
            "creator",
            "participants",
            "income",
            "expenses",
            "expenses_sum",
            "budget_left",
        )

    def sum_up_expenses(self, budget):
        value = budget.expenses.aggregate(Sum("value"))["value__sum"]
        return value or 0

    def get_expenses_sum(self, budget):
        return self.sum_up_expenses(budget)

    def get_budget_left(self, budget):
        # income = budget.income.aggregate(Sum('value'))["value__sum"]
        income = Income.objects.filter(budget=budget).first()
        income = income.value if income else 0
        return income - self.sum_up_expenses(budget)


class BudgetDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["pk"]


class CategoryCreateSerializer(BudgetCreatorOrParticipantMixin, serializers.ModelSerializer):
    remove_creator = True

    class Meta:
        model = Category
        fields = ["name", "budget"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("pk", "name")


class CategoryListSerializer(BudgetCreatorOrParticipantMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["budget"]


class CategoryEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "name"]

    def has_access(self, instance):
        user = self._context["request"].user
        if (
            instance.budget.creator != user
            or user not in instance.budget.participants.all()
        ):
            raise PermissionDenied(
                "Only Budget Creator or Participant can edit Category"
            )

    def update(self, instance, validated_data):
        self.has_access(instance)
        return super().update(instance, validated_data)


class CategoryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk"]
