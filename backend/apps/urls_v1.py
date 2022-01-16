from budget import urls as budget_urls
from django.conf.urls import include
from django.urls import path
from friends import urls as friends_urls

urlpatterns = [
    path("", include("users.urls")),
    path("friends/", include((friends_urls, "friends"), namespace="friends")),
    path("budget/", include((budget_urls, "budget"), namespace="budget")),
]
