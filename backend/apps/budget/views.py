
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Budget
from .serializers import BudgetCreateSerializer


PAGINATE_BY = settings.PAGINATE_BY


class BudgetCreate(CreateAPIView):
    model = Budget
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetCreateSerializer

    def create(self, request, *args, **kwargs):
        request.data['creator'] = request.user.id
        return super().create(request, *args, **kwargs)
