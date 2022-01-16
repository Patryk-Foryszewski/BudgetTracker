from django.conf.urls import include
from django.urls import path
from friends import urls as friends_urls

urlpatterns = [
    path("", include("users.urls")),
    path("friends/", include((friends_urls, "friends"), namespace="friends")),
]
