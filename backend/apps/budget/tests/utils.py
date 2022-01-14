from django.test import RequestFactory, TestCase
from faker import Factory

from .mixins import ValidationErrorTestMixin

fake = Factory.create()

request_factory = RequestFactory()


class ModelTester(ValidationErrorTestMixin, TestCase):
    """Combines ValidationErrorTestMixin with TestCase.

    Adds "assert_validation_errors" method to validate
    if required fields are filled

    """
