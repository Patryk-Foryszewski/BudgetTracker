from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Budget


class HasAccessMixin:
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        budget = validated_data["budget"].id
        user = validated_data["creator"].id
        creator_or_participant = Budget.objects.filter(
            Q(pk=budget) & (Q(creator=user) | Q(participants=user))
        ).first()

        if not creator_or_participant:
            raise PermissionDenied(
                "User not allowed to create expenses for this budget"
            )
        return validated_data


class AddCreatorMixin:
    def validate(self, attrs):
        validated = super().validate(attrs)
        creator = self._context["request"].user
        validated["creator"] = creator
        return validated
