import json

from django.test import TestCase
from faker import Faker
from rest_framework import status
from rest_framework.test import force_authenticate

from ..views import BudgetCreate
from .factories import UserFactory
from .utils import request_factory


class CreateBudgetView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()

    def test_unauthenticated_user(self):
        request = request_factory.post("/")
        request.user = self.user
        response = BudgetCreate.as_view()(request)
        self.assertEqual(403, response.status_code)

    def test_required_field_name(self):
        request = request_factory.post("/", data={}, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = BudgetCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("required", str(response.data["name"][0].code))

    def test_name_can_not_be_blank(self):
        request = request_factory.post(
            "/", data={"name": ""}, content_type="application/json"
        )
        force_authenticate(request, user=self.user)
        response = BudgetCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("blank", str(response.data["name"][0].code))

    def test_create_budget_and_assign_user(self):
        fake = Faker(["pl_PL", "la"])
        data = {
            "name": fake.sentence(nb_words=1),
            "content": fake.sentence(nb_words=30, variable_nb_words=False),
        }

        request = request_factory.post(
            "/", data=json.dumps(data), content_type="application/json"
        )
        force_authenticate(request, user=self.user)
        response = BudgetCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


