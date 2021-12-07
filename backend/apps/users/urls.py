from django.conf.urls import include
from django.urls import path
from django.contrib.auth import logout


urlpatterns = [
    path("logout/", logout, {'next_page': '/'}, name='logout'),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
