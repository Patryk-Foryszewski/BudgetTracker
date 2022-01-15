from apps.budget.tests.utils import request_factory
from apps.users.tests.factories import UserFactory
from django.test import TestCase
from rest_framework import status
from rest_framework.test import force_authenticate

from ..views import UserProfile


class Profile(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()

    def test_unauthenticated_user(self):
        request = request_factory.get("/")
        response = UserProfile.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_fields(self):
        request = request_factory.get("/")
        force_authenticate(request, self.user)
        response = UserProfile.as_view()(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
