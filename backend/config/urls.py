from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="FamilyBudget API",
        default_version="v1",
        description="""Application that allows user to create bugdets and track its expenses.
                       The application allows for creating several users. Each user can
                       create a list of any number of budgets and share it with any
                       number of users. The budget consists of income and expenses.
                       They are grouped into categories.""",
        terms_of_service="not_yet",
        contact=openapi.Contact(email="patryk.foryszewski@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", RedirectView.as_view(url="docs")),
    path("docs", schema_view.with_ui(cache_timeout=0), name="docs"),
    path("admin/", admin.site.urls, name="admin"),
    path("api/v1/", include("apps.urls_v1")),
]
