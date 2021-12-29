from django.contrib.auth import get_user_model
from django.db.models import Sum
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


class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("name", "budget", "value", "creator")


class ExpenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("name", "value")


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
