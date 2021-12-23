from rest_framework.exceptions import ValidationError


def disallow_empty_string(string):
    if not string:
        raise ValidationError("name can not be empty")
    return string
