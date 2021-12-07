from datetime import date

from factory import Faker, Sequence
from factory.django import DjangoModelFactory

from ..models import Budget
from apps.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = Faker('name')
    email = Faker('email')


class BudgetFactory(DjangoModelFactory):
    class Meta:
        model = Budget

    name = Faker('sentence', nb_words=1)

