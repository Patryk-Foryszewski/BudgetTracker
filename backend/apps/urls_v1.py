from django.conf.urls import include
from django.urls import path
from django.contrib.auth import logout


urlpatterns = [
    path('', include('users.urls')),
]
