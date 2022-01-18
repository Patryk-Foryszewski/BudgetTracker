from django.urls import path

from .views import (
    BudgetCreate,
    BudgetDelete,
    BudgetDetail,
    BudgetList,
    BudgetRemoveParticipants,
    BudgetUpdate,
    CategoryCreate,
    CategoryDelete,
    CategoryEdit,
    CategoryList,
    ExpenseCreate,
    ExpenseUpdate,
)

urlpatterns = [
    path("create/", BudgetCreate.as_view(), name="create"),
    path("<int:pk>/update/", BudgetUpdate.as_view(), name="update"),
    path("list/", BudgetList.as_view(), name="list"),
    path("<int:pk>/detail/", BudgetDetail.as_view(), name="detail"),
    path("<int:pk>/delete/", BudgetDelete.as_view(), name="delete"),
    path(
        "<int:pk>/remove_participants/",
        BudgetRemoveParticipants.as_view(),
        name="remove_participants",
    ),
    path(
        "<int:budget>/create_expense/", ExpenseCreate.as_view(), name="create_expense"
    ),
    path("update_expense/<int:pk>/", ExpenseUpdate.as_view(), name="update_expense"),
    path(
        "<int:budget>/create_category/",
        CategoryCreate.as_view(),
        name="create_category",
    ),
    path("<int:budget>/list_category/", CategoryList.as_view(), name="list_category"),
    path("edit_category/<int:pk>/", CategoryEdit.as_view(), name="edit_category"),
    path("delete_category/<int:pk>/", CategoryDelete.as_view(), name="delete_category"),
]
