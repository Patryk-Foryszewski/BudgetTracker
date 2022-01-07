from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Budget


class AddCreatorMixin:
    def validate(self, attrs):
        validated = super().validate(attrs)
        user = self._context["request"].user
        validated["creator"] = user
        return validated


class BudgetCreatorOrParticipantMixin(AddCreatorMixin):
    def has_access(self, user, budget):
        creator_or_participant = Budget.objects.filter(
            Q(pk=budget) & (Q(creator=user) | Q(participants=user))
        ).first()

        if not creator_or_participant:
            raise PermissionDenied(
                "Only Creator od Participant of Budget can perform this action"
            )

    def _remove_creator(self, validated_data):
        if getattr(self, "remove_creator", False):
            validated_data.pop("creator")

    def create(self, validated_data):
        self.has_access(validated_data["creator"].id, validated_data["budget"].id)
        self._remove_creator(validated_data)
        return super().create(validated_data)


class InstanceOrBudgetCreatorMixin(AddCreatorMixin):
    def has_access(self, instance, validated_data):

        if (
            validated_data["creator"] != instance.creator
            or validated_data["creator"] != instance.budget.creator
        ):
            raise PermissionDenied(
                "Only Instance Creator or Budget Creator can perform update"
            )

    def update(self, instance, validated_data):
        self.has_access(instance, validated_data)
        return super().update(instance, validated_data)
