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
    class Meta:
        model = Expense

    name = Faker("sentence", nb_words=1)
    value = Faker(
        "pydecimal", left_digits=6, right_digits=2, min_value=0, max_value=100000
    )
