from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q, Sum
from rest_framework import serializers

from .mixins import AddCreatorMixin
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
        fields = ["name", "content"]

    def has_access(self, instance, validated_data):

        if validated_data["creator"] != instance.creator:
            raise PermissionDenied("Only Budget Creator can edit Expense")

    def update(self, instance, validated_data):
        self.has_access(instance, validated_data)
        return super().update(instance, validated_data)


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


class ExpenseUpdateSerializer(AddCreatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("name", "value")

    def has_access(self, instance, validated_data):

        if (
            validated_data["creator"] != instance.creator
            or validated_data["creator"] != instance.budget.creator
        ):
            raise PermissionDenied(
                "Only Expense Creator or Budget Creator can edit Expense"
            )

    def update(self, instance, validated_data):
        # print('EXPENSE UPDATE SERIALIZER', instance, "|", validated_data)
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


class BudgetDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["pk"]


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name", "budget", "expenses"]

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        # Approach 1
        if validated_data.get('expenses'):
            for expense in validated_data['expenses']:
                if not validated_data['budget'].expenses.filter(id=expense.id):
                    raise ValidationError(f'This expense: {expense} is not related to given budget')
        # Approach 2
        # if validated_data.get('expenses'):
        #     budget_expenses = validated_data['budget'].expenses.all()
        #     for expense in validated_data['expenses']:
        #         if expense not in budget_expenses:
        #             raise ValidationError(f'This expense: {expense} is not related to given budget')

        return validated_data


class CategoryEditSerializer(AddCreatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "name"]

    def has_access(self, instance, validated_data):

        if (
            instance.budget.creator != validated_data['creator']
            or validated_data['creator'] not in instance.budget.participants.all()
        ):
            raise PermissionDenied(
                "Only Budget Creator or Participant can edit Category"
            )

    def update(self, instance, validated_data):
        print('CATEGORY UPDATE', validated_data)
        self.has_access(instance, validated_data)
        return super().update(instance, validated_data)


class CategoryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk"]


class CategoryDeleteBindingSerializer(AddCreatorMixin, serializers.ModelSerializer):
    expense = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ["pk", "expense"]

    def get_expense(self, *_):
        return self._context['request'].data['expense']

    def has_access(self, instance, validated_data):
        if (
            instance.budget.creator != validated_data['creator']
            and validated_data['creator'] not in instance.budget.participants.all()
        ):
            raise PermissionDenied(
                "Only Budget Creator or Participant can remove Category binding"
            )

    def validate(self, attrs):
        try:
            self._context['request'].data['expense']
        except KeyError as ke:
            raise ValidationError(message=f"Missing required key {ke}", code="required")
        validated_data = super().validate(attrs)
        print('VALIDATE', attrs)
        return validated_data

    def update(self, instance, validated_data):
        print('REMOVE BINDING', instance, "|", validated_data)
        self.has_access(instance, validated_data)
        # instance.expenses.remove(self.get_expense())
        # instance.save()
        return instance
