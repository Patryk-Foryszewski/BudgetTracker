from django.conf import settings
from django.db.models import Q
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import Budget, Expense
from .serializers import (
    BudgetCreateSerializer,
    BudgetDetailSerializer,
    BudgetListSerializer,
    BudgetUpdateSerializer,
    ExpenseCreateSerializer,
    ExpenseUpdateSerializer,
)

PAGINATE_BY = settings.PAGINATE_BY


class BudgetCreate(CreateAPIView):
    model = Budget
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetCreateSerializer


class BudgetList(ListAPIView):
    paginate_by = PAGINATE_BY
    model = Budget
    ordering = ["created_date"]
    serializer_class = BudgetListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_budgets = self.model.objects.filter(
            Q(creator=self.request.user) | Q(participants=self.request.user)
        ).all()

        return user_budgets


class BudgetUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetUpdateSerializer
    queryset = Budget.objects.all()
    model = Budget


class BudgetDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetDetailSerializer
    queryset = Budget.objects.all()
    model = Budget


class ExpenseCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseCreateSerializer
    model = Expense


class ExpenseUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseUpdateSerializer
    queryset = Expense.objects.all()
    model = Expense
