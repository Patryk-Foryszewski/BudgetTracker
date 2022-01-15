from contextlib import contextmanager

from django.core.exceptions import ValidationError


class ValidationErrorTestMixin(object):
    @contextmanager
    def assert_validation_errors(self, fields):
        """Validate required fields.

        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))
        else:
            raise AssertionError("ValidationError not raised")
