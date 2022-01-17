from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Sum
from rest_framework import serializers
from users.serializers import UserLimitedSerializer

from .mixins import (
    AddCreatorMixin,
    BudgetCreatorOrParticipantMixin,
    InstanceOrBudgetCreatorMixin,
)
from .models import Budget, Category, Expense, Income

User = get_user_model()


class BudgetCreateSerializer(AddCreatorMixin, serializers.ModelSerializer):
    # creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ["name", "content", "participants"]


class UserListingField(serializers.RelatedField):
    def to_representation(self, user):
        return user.username


class BudgetListSerializer(serializers.ModelSerializer):
    creator = UserLimitedSerializer()  # UserListingField(queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ["pk", "name", "creator"]


class BudgetUpdateSerializer(AddCreatorMixin, serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=Budget._meta.get_field("name").max_length, required=False
    )

    class Meta:
        model = Budget
        fields = ["name", "content"]

    def has_access(self, instance, validated_data):
        if validated_data["creator"] != instance.creator:
            raise PermissionDenied("Only Budget Creator can edit Budget")

    def update(self, instance, validated_data):
        self.has_access(instance, validated_data)
        return super().update(instance, validated_data)


class BudgetRemoveParticipantsSerializer(
    InstanceOrBudgetCreatorMixin, serializers.ModelSerializer
):
    class Meta:
        model = Budget
        fields = ["participants"]

    def update(self, instance, validated_data):
        self.has_access(instance, validated_data)
        for participant in validated_data["participants"]:
            instance.participants.remove(participant)
        instance.save()
        return instance


class ExpenseSerializer(serializers.ModelSerializer):
    creator = UserLimitedSerializer()

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


class ExpenseCreateSerializer(
    BudgetCreatorOrParticipantMixin, serializers.ModelSerializer
):
    class Meta:
        model = Expense
        fields = ("name", "budget", "value", "category")


class ExpenseUpdateSerializer(
    InstanceOrBudgetCreatorMixin, serializers.ModelSerializer
):
    name = serializers.CharField(
        max_length=Expense._meta.get_field("name").max_length, required=False
    )

    class Meta:
        model = Expense
        fields = ("name", "value", "category")


class IncomeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ("name", "value")


class IncomeSerializer(serializers.ModelSerializer):
    creator = UserLimitedSerializer()

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
    creator = UserLimitedSerializer()
    income = IncomeSerializer(many=True)
    expenses = serializers.SerializerMethodField(
        "paginated_expenses"
    )  # ExpenseSerializer(many=True)
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

    def paginated_expenses(self, budget):
        size = self.context["view"].kwargs.get(
            "size", settings.REST_FRAMEWORK["PAGE_SIZE"]
        )
        paginator = Paginator(budget.expenses.all().order_by("-created_date"), size)
        page = self.context["view"].kwargs.get("page", 1)
        try:
            tracks = paginator.page(page)
        except EmptyPage:
            tracks = paginator.page(1)

        serializer = ExpenseSerializer(tracks, many=True)
        return serializer.data


class BudgetDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["pk"]


class CategoryCreateSerializer(
    BudgetCreatorOrParticipantMixin, serializers.ModelSerializer
):
    remove_creator = True

    class Meta:
        model = Category
        fields = ["name", "budget"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("pk", "name")


class CategoryListSerializer(
    BudgetCreatorOrParticipantMixin, serializers.ModelSerializer
):
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
            and user not in instance.budget.participants.all()
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
