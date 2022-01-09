from apps.users.models import User
from factory import Faker
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("name")
    email = Faker("email")
