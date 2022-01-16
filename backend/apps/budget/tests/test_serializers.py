from apps.users.tests.factories import UserFactory
from django.test import TestCase
from faker import Faker

from ..serializers import (
    BudgetCreateSerializer,
    BudgetListSerializer,
    CategoryListSerializer,
)
from .factories import BudgetFactory
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
        context = {"request": request}

        cls.serializer = BudgetCreateSerializer(
            data=cls.budget_attributes, context=context
        )

    def test_contains_expected_fields(self):
        self.serializer.is_valid()
        data = self.serializer.data

        self.assertEqual(list(data.keys()), ["name", "content"])


class BudgetListSerializerTester(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user = UserFactory()
        budget = BudgetFactory(creator=cls.user)
        cls.serializer = BudgetListSerializer(
            data={"pk": budget.pk, "creator": cls.user, "name": "family"}
        )

    def test_contains_expected_fields(self):
        self.serializer.is_valid()
        data = self.serializer.data

        self.assertEqual(list(data.keys()), ["name", "creator"])


class CategoryListSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.creator = UserFactory()
        cls.attributes = {"budget": "1"}
        request = request_factory.post("/")
        request.user = cls.creator
        context = {"request": request}

        cls.serializer = CategoryListSerializer(data=cls.attributes, context=context)

    def test_contains_expected_fields(self):
        self.serializer.is_valid()
        data = self.serializer.data

        self.assertEqual(list(data.keys()), ["budget"])
