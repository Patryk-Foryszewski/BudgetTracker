from django.urls import path
from django.contrib import admin
from django.contrib.auth import logout

from django.conf.urls import include

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("api/v1/", include("apps.urls_v1")),
]
