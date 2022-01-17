from django.urls import path

from .views import BudgetCreate, BudgetList

urlpatterns = [
    path("create/", BudgetCreate.as_view(), name="create"),
    path("list/", BudgetList.as_view(), name="list"),
]
