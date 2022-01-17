from django.urls import path

from .views import BudgetCreate, BudgetList, BudgetUpdate

urlpatterns = [
    path("create/", BudgetCreate.as_view(), name="create"),
    path("update/", BudgetUpdate.as_view(), name="update"),
    path("list/", BudgetList.as_view(), name="list"),
]
