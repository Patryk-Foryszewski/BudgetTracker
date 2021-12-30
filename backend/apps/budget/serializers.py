from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Sum
from rest_framework import serializers

from .mixins import AddCreatorMixin
from .models import Budget, Expense, Income

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


class BudgetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["name"]


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


class ExpenseCreateSerializer(AddCreatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("name", "budget", "value")

    def has_access(self, validated_data):
        creator_or_participant = Budget.objects.filter(
            Q(pk=validated_data["budget"].id)
            & (
                Q(creator=validated_data["creator"].id)
                | Q(participants=validated_data["creator"].id)
            )
        ).first()

        if not creator_or_participant:
            raise PermissionDenied(
                "User not allowed to create expenses for this budget"
            )

    def create(self, validated_data):
        self.has_access(validated_data)
        return super().create(validated_data)


class ExpenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("creator", "name", "value")

    def has_access(self, instance, validated_data):
        creator = self._context["request"].user
        validated_data["creator"] = creator
        if (
            validated_data["creator"] != instance.creator
            or validated_data["creator"] != instance.budget.creator
        ):
            raise PermissionDenied(
                "Only Expense Creator or Budget Creator can edit Expense"
            )

    def update(self, instance, validated_data):
        self.has_access(instance, validated_data)
        return super().update(instance, validated_data)


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
