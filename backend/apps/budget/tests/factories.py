from django.conf import settings
from factory import Faker
from factory.django import DjangoModelFactory

from ..models import Budget, Expense

User = settings.AUTH_USER_MODEL


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("name")
    email = Faker("email")


class BudgetFactory(DjangoModelFactory):
    class Meta:
        model = Budget

    name = Faker("sentence", nb_words=1)


class ExpenseFactory(DjangoModelFactory):
    name = Faker("sentence", nb_words=1)

    class Meta:
        model = Expense
