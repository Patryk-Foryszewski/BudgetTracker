from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth import logout
from django.urls import path

from .views import UserProfile, UsersList

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("logout/", logout, {"next_page": "/"}, name="logout"),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("users/profile", UserProfile.as_view(), name="user_profile"),
    path("users/list", UsersList.as_view(), name="users_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
