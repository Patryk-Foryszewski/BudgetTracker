from django.urls import path

from .views import BudgetCreate

urlpatterns = [
    path("create/", BudgetCreate.as_view(), name="create_budget"),
]
