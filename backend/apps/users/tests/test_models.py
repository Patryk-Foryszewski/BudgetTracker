from apps.budget.tests.utils import ModelTester
from apps.users.models import User


class TestUser(ModelTester):
    @classmethod
    def setUpTestData(cls):
        cls.model = User

    def test_required_model_fields(self):
        # self.instance = self.model.objects.create()
        with self.assert_validation_errors(["username", "email", "password"]):
            self.model.objects.create()

    def test_get_avatar(self):
        user = self.model.objects.create(
            username="Joe Dohn", email="jd@dj.com", password="1234"
        )
        user.refresh_from_db()
        print("Avatar", user.avatar)
