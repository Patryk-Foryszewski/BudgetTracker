from django.urls import path

from .views import (
    BudgetCreate,
    BudgetDelete,
    BudgetDetail,
    BudgetList,
    BudgetRemoveParticipants,
    BudgetUpdate,
    CategoryCreate,
    CategoryEdit,
    CategoryList,
    ExpenseCreate,
    ExpenseUpdate,
)

urlpatterns = [
    path("create/", BudgetCreate.as_view(), name="create"),
    path("update/<int:pk>/", BudgetUpdate.as_view(), name="update"),
    path("list/", BudgetList.as_view(), name="list"),
    path("detail/<int:pk>/", BudgetDetail.as_view(), name="detail"),
    path("delete/<int:pk>/", BudgetDelete.as_view(), name="delete"),
    path(
        "remove_participants/<int:pk>/",
        BudgetRemoveParticipants.as_view(),
        name="remove_participants",
    ),
    path(
        "create_expense/<int:budget>/", ExpenseCreate.as_view(), name="create_expense"
    ),
    path("update_expense/<int:pk>/", ExpenseUpdate.as_view(), name="update_expense"),
    path(
        "create_category/<int:budget>/",
        CategoryCreate.as_view(),
        name="create_category",
    ),
    path("list_category/<int:budget>/", CategoryList.as_view(), name="list_category"),
    path("edit_category/<int:pk>/", CategoryEdit.as_view(), name="edit_category"),
]
