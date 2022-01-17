from django.urls import path

from .views import (
    BudgetCreate,
    BudgetDetail,
    BudgetList,
    BudgetRemoveParticipants,
    BudgetUpdate,
    ExpenseCreate,
)

urlpatterns = [
    path("create/", BudgetCreate.as_view(), name="create"),
    path("update/", BudgetUpdate.as_view(), name="update"),
    path("list/", BudgetList.as_view(), name="list"),
    path("detail/", BudgetDetail.as_view(), name="detail"),
    path(
        "remove_participants/",
        BudgetRemoveParticipants.as_view(),
        name="remove_participants",
    ),
    path("create_expense/", ExpenseCreate.as_view(), name="create_expense"),
]
