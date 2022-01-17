import json

from apps.users.tests.factories import UserFactory
from django.test import TestCase
from faker import Faker
from rest_framework import status
from rest_framework.test import force_authenticate

from ..models import Budget
from ..views import (
    BudgetCreate,
    BudgetDelete,
    BudgetDetail,
    BudgetList,
    BudgetRemoveParticipants,
    BudgetUpdate,
    CategoryCreate,
    CategoryDelete,
    CategoryEdit,
    CategoryList,
    ExpenseCreate,
    ExpenseUpdate,
)
from .factories import BudgetFactory, CategoryFactory, ExpenseFactory
from .utils import request_factory


class CreateBudget(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()

    def test_unauthenticated_user(self):
        request = request_factory.post("/")
        response = BudgetCreate.as_view()(request)
        self.assertEqual(401, response.status_code)
        self.assertEqual(response.data["detail"].code, "not_authenticated")

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

    def test_create_budget_and_add_creator(self):
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
        participants = Budget.objects.all().first().participants.all()
        self.assertEqual(len(participants), 3)


class UpdateBudget(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.user_2 = UserFactory()
        cls.participant = UserFactory()
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

    def test_update_add_participant(self):
        data = {"participants": [str(self.participant.id)]}
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = BudgetUpdate.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_budget_by_user_that_is_not_creator_or_participant(self):
        fake = Faker(["pl_PL", "la"])
        data = {"name": fake.sentence(nb_words=1)}
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_2)
        response = BudgetUpdate.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RemoveBudgetParticipant(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.creator = UserFactory()
        participant1 = UserFactory()
        cls.participant2 = UserFactory()
        participant3 = UserFactory()
        cls.budget = BudgetFactory(creator=cls.creator)
        cls.budget.participants.set([participant1, cls.participant2, participant3])

    def test_remove_participant(self):
        data = {"participants": [str(self.participant2.id)]}
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.creator)
        response = BudgetRemoveParticipants.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BudgetListView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = UserFactory()

    def test_unauthenticated_user(self):
        request = request_factory.post("/")
        response = BudgetList.as_view()(request)
        self.assertEqual(401, response.status_code)
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_list_for_creator_field(self):
        budgets_quantity = 4
        for _ in range(budgets_quantity):
            BudgetFactory(creator=self.user1)
        request = request_factory.get("/")
        force_authenticate(request, user=self.user1)
        response = BudgetList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(budgets_quantity, len(response.data))
        self.assertListEqual(
            list(dict(response.data["results"][0]).keys()), ["pk", "name", "creator"]
        )


class DetailBudget(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.budget = BudgetFactory(creator=cls.user)
        cls.expense_1 = ExpenseFactory(
            budget=cls.budget, creator=cls.user, value="10.41"
        )
        cls.expense_2 = ExpenseFactory(
            budget=cls.budget, creator=cls.user, value="15.74"
        )
        cls.expense_3 = ExpenseFactory(
            budget=cls.budget, creator=cls.user, value="21.13"
        )
        cls.expense_4 = ExpenseFactory(
            budget=cls.budget, creator=cls.user, value="62.90"
        )

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
        self.assertListEqual(keys, list(response.data.keys()))

    def test_first_page_paginator(self):
        request = request_factory.get("/", content_type="application/json")
        force_authenticate(request, user=self.user)
        response = BudgetDetail.as_view()(request, pk=self.budget.pk)
        self.assertEqual(4, len(response.data["expenses"]))

    def test_second_page_paginator(self):
        request = request_factory.get({"page": 2})
        force_authenticate(request, user=self.user)
        response = BudgetDetail.as_view()(request, pk=self.budget.pk, page=2)
        self.assertEqual(4, len(response.data["expenses"]))


class DeleteBudget(TestCase):
    def setUp(self) -> None:
        self.creator = UserFactory()
        self.user_2 = UserFactory()
        self.budget = BudgetFactory(creator=self.creator)

    def test_delete_by_unauthenticated_user(self):
        request = request_factory.post("/")
        response = BudgetDelete.as_view()(request)
        self.assertEqual(401, response.status_code)
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_delete_by_creator(self):
        request = request_factory.delete("/", content_type="application/json")
        force_authenticate(request, user=self.creator)
        response = BudgetDelete.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_by_user_that_is_not_creator(self):
        request = request_factory.delete("/", content_type="application/json")
        force_authenticate(request, user=self.user_2)
        response = BudgetDelete.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"].code, "permission_denied")


class CreateExpense(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = UserFactory()
        cls.user_2 = UserFactory()
        cls.budget = BudgetFactory(creator=cls.user_1)
        # cls.expense = ExpenseFactory(creator=cls.user, budget=cls.budget)

    def test_create_expense_without_required_keys(self):
        fake = Faker(["pl_PL", "la"])

        data = {"name": fake.sentence(nb_words=1), "value": 10.41}
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
            "value": 10.41,
        }
        request = request_factory.post("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_1)

        response = ExpenseCreate.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_expense_with_assigned_category(self):
        category = CategoryFactory(budget=self.budget)
        fake = Faker(["pl_PL", "la"])
        data = {
            "name": fake.sentence(nb_words=1),
            "budget": self.budget.pk,
            "value": 10,
            "category": str(category.id),
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
        cls.user_3 = UserFactory()
        cls.budget = BudgetFactory(creator=cls.user_1)
        cls.expense = ExpenseFactory(creator=cls.user_1, budget=cls.budget)

    def test_update_expense_by_creator(self):
        fake = Faker(["pl_PL", "la"])
        data = {
            "name": fake.sentence(nb_words=1),
            "budget": self.budget.pk,
            "value": 10,
        }
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_1)

        response = ExpenseUpdate.as_view()(request, pk=self.expense.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_expense_by_not_creator_or_participant(self):
        fake = Faker(["pl_PL", "la"])
        data = {
            "name": fake.sentence(nb_words=1),
            "budget": self.budget.pk,
            "value": 10,
        }
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_2)

        response = ExpenseUpdate.as_view()(request, pk=self.expense.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateCategory(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.budget = BudgetFactory(creator=cls.user)

    def test_unauthenticated_user(self):
        request = request_factory.post("/")
        response = CategoryCreate.as_view()(request)
        self.assertEqual(401, response.status_code)
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_required_field_name(self):
        request = request_factory.post("/", data={}, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = BudgetCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("required", str(response.data["name"][0].code))

    def test_required_field_budget(self):
        request = request_factory.post(
            "/", data={"name": "fruits"}, content_type="application/json"
        )
        force_authenticate(request, user=self.user)
        response = CategoryCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("required", str(response.data["budget"][0].code))

    def test_create_category_with_valid_data(self):
        data = {"name": "fruits", "budget": self.budget.id}
        request = request_factory.post("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = CategoryCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ListCategory(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.creator = UserFactory()
        cls.user_2 = UserFactory()
        cls.budget = BudgetFactory(creator=cls.creator)
        cls.category_1 = CategoryFactory(name="fruits", budget=cls.budget)
        cls.category_2 = CategoryFactory(name="parts", budget=cls.budget)
        cls.category_3 = CategoryFactory(name="cheeses", budget=cls.budget)

    def test_delete_by_unauthenticated_user(self):
        request = request_factory.post("/")
        response = CategoryDelete.as_view()(request)
        self.assertEqual(401, response.status_code)
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_list_categories_for_given_budget(self):
        data = {"budget": str(self.budget.id)}

        request = request_factory.get("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.creator)
        response = CategoryList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_categories_by_user_that_is_not_budget_creator_or_participant(self):
        data = {"budget": str(self.budget.id)}
        request = request_factory.get("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_2)
        response = CategoryList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EditCategory(TestCase):
    def setUp(self) -> None:
        self.creator = UserFactory()
        self.user_2 = UserFactory()
        self.budget = BudgetFactory(creator=self.creator)
        self.category = CategoryFactory(name="fruits", budget=self.budget)

    def test_edit_by_unauthenticated_user(self):
        request = request_factory.post("/")
        response = CategoryEdit.as_view()(request)
        self.assertEqual(401, response.status_code)
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_edit_category_by_user_that_is_not_budget_creator_or_participant(self):
        data = {"name": "tools"}
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user_2)
        response = CategoryEdit.as_view()(request, pk=self.category.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_category_name(self):
        data = {"name": "tools"}
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.creator)
        response = CategoryEdit.as_view()(request, pk=self.category.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteCategory(TestCase):
    def setUp(self) -> None:
        self.creator = UserFactory()
        self.user_2 = UserFactory()
        self.budget = BudgetFactory(creator=self.creator)
        self.category = CategoryFactory(budget=self.budget)

    def test_delete_by_unauthenticated_user(self):
        request = request_factory.post("/")
        response = CategoryDelete.as_view()(request)
        self.assertEqual(401, response.status_code)
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_delete_by_creator_of_budget(self):
        request = request_factory.delete("/", content_type="application/json")
        force_authenticate(request, user=self.creator)
        response = CategoryDelete.as_view()(request, pk=self.category.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_by_user_that_is_not_creator_of_budget(self):
        request = request_factory.delete("/", content_type="application/json")
        force_authenticate(request, user=self.user_2)
        response = CategoryDelete.as_view()(request, pk=self.budget.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"].code, "permission_denied")
