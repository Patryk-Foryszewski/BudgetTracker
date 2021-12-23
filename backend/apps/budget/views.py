from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Budget
from .serializers import BudgetSerializer, BudgetCreateSerializer, BudgetListSerializer
from django.contrib.auth import get_user_model

PAGINATE_BY = settings.PAGINATE_BY


class BudgetCreate(CreateAPIView):
    model = Budget
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetCreateSerializer

    def create(self, request, *args, **kwargs):
        request.data['creator'] = request.user.id
        return super().create(request, *args, **kwargs)


class BudgetList(ListAPIView):
    paginate_by = PAGINATE_BY
    model = Budget
    ordering = ["created_date"]
    serializer_class = BudgetListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        creator = self.model.objects.filter(creator=self.request.user)
        participant = self.model.objects.filter(participants=self.request.user)
        return creator.union(participant)
