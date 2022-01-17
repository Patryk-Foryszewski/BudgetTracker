from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .mixins import BudgetCreatorOrParticipantMixin
from .models import Budget, Category, Expense
from .serializers import (
    BudgetCreateSerializer,
    BudgetDeleteSerializer,
    BudgetDetailSerializer,
    BudgetListSerializer,
    BudgetRemoveParticipantsSerializer,
    BudgetUpdateSerializer,
    CategoryCreateSerializer,
    CategoryDeleteSerializer,
    CategoryEditSerializer,
    CategorySerializer,
    ExpenseCreateSerializer,
    ExpenseUpdateSerializer,
)

PAGINATE_BY = settings.PAGINATE_BY


class BudgetCreate(CreateAPIView):
    """
    Endpoint for creating budget.

    ### Fields descriptions:

       * name: name of a budget.
       * content: text field for notes etc.
       * participants: list of users ids that will have access to the budget

    ### Reqired fields:

       * name

    ### Response status codes:

       * 201 OK CREATED
       * 400 BAD REQUEST. Wrong data, lack of required field.
       * 401 UNAUTHORIZED. Only logged used can create budget.

    ### Avalible methods:

       * POST
    """

    model = Budget
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetCreateSerializer


class BudgetList(ListAPIView):
    """
    Returns budgets for requesting user.

    ### Query params:

       * &page=x - specify page.

    ### Response status codes:

       * 201 OK CREATED
       * 401 UNAUTHORIZED. Only logged used can create budget.

    ### Avalible methods:

       * POST
    """

    model = Budget
    ordering = ["created_date"]
    serializer_class = BudgetListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_budgets = (
            self.model.objects.filter(
                Q(creator=self.request.user) | Q(participants=self.request.user)
            )
            .all()
            .order_by("-created_date")
        )

        return user_budgets


class BudgetUpdate(UpdateAPIView):
    """
    Endpoint for updating budget.

    ### Query params:

       * &pk=x - specify budget id.

    ### Response status codes:

       * 200 OK
       * 401 UNAUTHORIZED. Only logged used can update budget.
       * 403 FORBIDDEN. Only creator or participant can upadte

    ### Avalible methods:

       * PATCH
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BudgetUpdateSerializer
    queryset = Budget.objects.all()
    model = Budget


class BudgetDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetDetailSerializer
    queryset = Budget.objects.all()
    model = Budget


class BudgetRemoveParticipants(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetRemoveParticipantsSerializer
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


class BudgetDelete(DestroyAPIView):
    model = Budget
    queryset = Budget.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetDeleteSerializer

    def has_access(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied("Only Creator of Budget is allowed to delete")

    def perform_destroy(self, instance):
        self.has_access(instance)
        super().perform_destroy(instance)


class CategoryCreate(CreateAPIView):
    model = Category
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryCreateSerializer


class CategoryList(BudgetCreatorOrParticipantMixin, ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        budget = self.request.GET.get("budget")
        self.has_access(self.request.user, budget)
        return super().get_queryset()


class CategoryEdit(UpdateAPIView):
    model = Category
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryEditSerializer


class CategoryDelete(DestroyAPIView):
    model = Category
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryDeleteSerializer

    def has_access(self, instance):

        if (
            instance.budget.creator != self.request.user
            and self.request.user not in instance.budget.participants.all()
        ):
            raise PermissionDenied(
                "Only Creator or Participant of Budget is allowed to delete"
            )

    def perform_destroy(self, instance):
        self.has_access(instance)
        super().perform_destroy(instance)
