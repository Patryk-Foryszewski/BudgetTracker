from django.test import TestCase

from ..serializers import UserLimitedSerializer
from .factories import UserFactory


class UserLimitedSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.user.refresh_from_db()
        cls.serializer = UserLimitedSerializer(data=vars(cls.user))

    def test_contains_expected_fields(self):
        self.serializer.is_valid()
        data = self.serializer.data
        self.assertEqual(list(data.keys()), ["username", "avatar"])
