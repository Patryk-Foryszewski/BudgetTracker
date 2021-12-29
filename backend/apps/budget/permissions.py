from rest_framework.permissions import BasePermission

from .models import Budget


class HasAccessPermissions(BasePermission):
    message = ""

    def has_permission(self, request, view):
        serializer = view.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        budget = request.data["budget"]
        user = request.user
        creator = Budget.objects.filter(pk=budget, creator=user).first()
        participant = Budget.objects.filter(pk=budget, participants=user).first()
        if not creator or participant:
            self.message = "User not allowed to create expenses for this budget"
            return False
        return True
