from django.test import TestCase
from ..serializers import BudgetCreateSerializer, CategoryListSerializer
from ..models import Budget
from .factories import UserFactory
from faker import Faker
from rest_framework.test import force_authenticate
from .utils import request_factory


class BudgetCreateSerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        fake = Faker(["pl_PL", "la"])
        cls.creator = UserFactory()
        cls.budget_attributes = {
            "name": fake.sentence(nb_words=1),
            "content": fake.sentence(nb_words=30, variable_nb_words=False),
        }
        request = request_factory.post("/")
        request.user = cls.creator
        context = {
            'request': request
        }

        cls.serializer = BudgetCreateSerializer(data=cls.budget_attributes, context=context)

    def test_contains_expected_fields(self):
        self.serializer.is_valid()
        data = self.serializer.data

        self.assertEqual(list(data.keys()), ['name', 'content'])


class CategoryListSerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        fake = Faker(["pl_PL", "la"])
        cls.creator = UserFactory()
        cls.attributes = {
            "budget": "1"
        }
        request = request_factory.post("/")
        request.user = cls.creator
        context = {
            'request': request
        }

        cls.serializer = CategoryListSerializer(data=cls.attributes, context=context)

    def test_contains_expected_fields(self):
        self.serializer.is_valid()
        data = self.serializer.data

        self.assertEqual(list(data.keys()), ['budget'])
