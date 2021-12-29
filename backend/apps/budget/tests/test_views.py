import json

from django.test import TestCase
from faker import Faker
from rest_framework import status
from rest_framework.test import force_authenticate

from ..views import BudgetCreate, BudgetDetail, BudgetList, BudgetUpdate, ExpenseCreate
from .factories import BudgetFactory, UserFactory
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

    def test_add_participants_to_budget(self):
        fake = Faker(["pl_PL", "la"])
        participant1 = UserFactory()
        participant2 = UserFactory()
        participant3 = UserFactory()
        data = {
            "name": fake.sentence(nb_words=1),
            "content": fake.sentence(nb_words=30, variable_nb_words=False),
            "participants": [
                str(participant1.id),
                str(participant2.id),
                str(participant3.id),
            ],
        }
        request = request_factory.post(
            "/", data=json.dumps(data), content_type="application/json"
        )
        force_authenticate(request, user=self.user)
        response = BudgetCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BudgetListView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()

    def test_list_for_creator_field(self):
        budgets_quantity = 4
        for _ in range(budgets_quantity):
            BudgetFactory(creator=self.user1)
        request = request_factory.get("/")
        force_authenticate(request, user=self.user1)
        response = BudgetList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(budgets_quantity, len(response.data))


class UpdateBudget(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.budget = BudgetFactory(creator=cls.user)

    def test_update_budget_name(self):
        fake = Faker(["pl_PL", "la"])
        data = {"name": fake.sentence(nb_words=1)}
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = BudgetUpdate.as_view()(request, pk=self.budget.pk)
        self.budget.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.budget.name, data["name"])


class DetailBudget(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.budget = BudgetFactory(creator=cls.user)

    def test_details_keys(self):
        request = request_factory.get("/", content_type="application/json")
        force_authenticate(request, user=self.user)
        response = BudgetDetail.as_view()(request, pk=self.budget.pk)
        keys = [
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
        ]
        self.assertEqual(len(keys), len(response.data.keys()))

        # for key in keys:
        #     self.assertIn(key, response.data.keys())


class CreateExpense(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = UserFactory()
        cls.user_2 = UserFactory()
        cls.budget = BudgetFactory(creator=cls.user_1)
        # cls.expense = ExpenseFactory(creator=cls.user, budget=cls.budget)

    def test_create_expense_without_required_keys(self):
        fake = Faker(["pl_PL", "la"])

        data = {"name": fake.sentence(nb_words=1), "value": 10}
        request = request_factory.post("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_1)

        response = ExpenseCreate.as_view()(request, pk=self.budget.pk)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_expense_by_user_that_is_not_creator_or_participant(self):
        fake = Faker(["pl_PL", "la"])

        data = {
            "name": fake.sentence(nb_words=1),
            "budget": self.budget.pk,
            "value": 10,
        }
        request = request_factory.post("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_2)

        response = ExpenseCreate.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_expense(self):
        fake = Faker(["pl_PL", "la"])

        data = {
            "name": fake.sentence(nb_words=1),
            "budget": self.budget.pk,
            "value": 10,
        }
        request = request_factory.post("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_1)

        response = ExpenseCreate.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateExpense(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = UserFactory()
        cls.user_2 = UserFactory()
        cls.budget = BudgetFactory(creator=cls.user_1)

    def test_add_participants_to_budget(self):
        fake = Faker(["pl_PL", "la"])
        participant1 = UserFactory()
        participant2 = UserFactory()
        participant3 = UserFactory()
        data = {
            "name": fake.sentence(nb_words=1),
            "content": fake.sentence(nb_words=30, variable_nb_words=False),
            "participants": [
                str(participant1.id),
                str(participant2.id),
                str(participant3.id),
            ],
        }
        request = request_factory.post(
            "/", data=json.dumps(data), content_type="application/json"
        )
        force_authenticate(request, user=self.user)
        response = BudgetCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
