class FullCleanSaveMixin:
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class AddCreatorMixin:
    def validate(self, attrs):
        validated = super().validate(attrs)
        creator = self._context["request"].user
        validated["creator"] = creator
        return validated
