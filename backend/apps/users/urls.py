from django.conf.urls import include
from django.urls import path
from django.contrib.auth import logout
from . views import UsersList, UserProfile

urlpatterns = [
    path("logout/", logout, {'next_page': '/'}, name='logout'),
    path("auth", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path('users/profile', UserProfile.as_view(), name='user_profile'),
    path('users/list', UsersList.as_view(), name='users_list')
]
