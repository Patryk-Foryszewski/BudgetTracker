from contextlib import contextmanager

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Budget, Category, Expense, Income
from .factories import BudgetFactory, CategoryFactory, UserFactory


class ValidationErrorTestMixin(object):
    @contextmanager
    def assert_validation_errors(self, fields):
        """Validate required fields.

        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))
        else:
            raise AssertionError("ValidationError not raised")


class ModelTester(ValidationErrorTestMixin, TestCase):
    """Combines ValidationErrorTestMixin with TestCase.

    Adds "assert_validation_errors" method to validate
    if required fields are filled

    """


class BudgetModelTester(ModelTester):
    def test_budget_must_have_name_and_creator(self):
        with self.assert_validation_errors(["name", "creator"]):
            Budget.objects.create()

    def test_str_method(self):
        creator = UserFactory(username="Philip")
        name = "Service"
        budget = Budget.objects.create(name=name, creator=creator)
        supposed = f"Budget: [{name}, Creator: {creator}]"
        self.assertEqual(supposed, str(budget))


class IncomeModelTester(ModelTester):
    def test_expense_must_have_name_budget_and_expense(self):
        with self.assert_validation_errors(["name", "budget", "creator"]):
            Expense.objects.create()

    def test_str_method(self):
        creator = UserFactory(username="Philip")
        name = "Service"
        budget = BudgetFactory(creator=creator)
        income = Income.objects.create(name=name, creator=creator, budget=budget)

        supposed = (
            f"Income: [name: {income.name}, value: "
            f"{income.value}, creator: {income.creator}]"
        )
        self.assertEqual(supposed, str(income))


class ExpenseModelTester(ModelTester):
    def test_expense_must_have_name_budget_and_expense(self):
        with self.assert_validation_errors(["name", "budget", "creator"]):
            Expense.objects.create()

    def test_str_method(self):
        creator = UserFactory(username="Philip")
        name = "Service"
        budget = BudgetFactory(creator=creator)
        expense = Expense.objects.create(name=name, creator=creator, budget=budget)
        supposed = (
            f"Expense: [name: {expense.name}, value: {expense.value}, creator: "
            f"{expense.creator}, {expense.category}]"
        )
        self.assertEqual(supposed, str(expense))


class CategoryModelTester(ModelTester):
    def test_category_must_have_name_and_budget(self):
        with self.assert_validation_errors(["name", "budget"]):
            Category.objects.create()

    def test_str_method(self):
        creator = UserFactory(username="Philip")
        name = "Service"
        budget = BudgetFactory(creator=creator)
        category = CategoryFactory(name=name, budget=budget)
        supposed = f"Category: [name: {category.name}]"
        self.assertEqual(supposed, str(category))
