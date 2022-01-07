from contextlib import contextmanager

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Category


class ValidationErrorTestMixin(object):
    @contextmanager
    def assert_validation_errors(self, fields):
        """Validate required fields.

        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))


class CategoryModelTester(ValidationErrorTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """Create instance of Book model to perform tests."""

    def test_category_must_have_name_budget_and_expense(self):
        with self.assert_validation_errors(["name", "budget"]):
            Category.objects.create()


# class CreateInvalidBook(ValidationErrorTestMixin, TestCase):
#     def test_book_must_have_title_and_author(self):
#         book = Book(
#             title="",
#             author="",
#             published_date="2008-10-15",
#             pages="",
#             isbn_10="",
#             isbn_13="9788389192868",
#             cover_uri="image.jpg",
#             language="en",
#         )
#
#         with self.assert_validation_errors(["title", "author", "slug"]):
#             book.full_clean()
