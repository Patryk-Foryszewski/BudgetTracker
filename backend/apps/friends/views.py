from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Friends
from .serializers import (
    FriendsAddSerializer,
    FriendsRemoveSerializer,
    FriendsSerializer,
)

User = get_user_model()


class FriendsAdd(UpdateAPIView):
    """Endpoint for adding firends to list.

    Send one or more user id to add them
    to friends_list"""

    model = Friends
    queryset = Friends.objects.all()
    serializer_class = FriendsAddSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    def get_object(self):
        return Friends.objects.get_or_create(user=self.request.user)[0]


class FriendsRemove(FriendsAdd):
    """Endpoint for removing firends from list.

    Send one or more user pk to remove them
    from firends_list"""

    serializer_class = FriendsRemoveSerializer

    def get_object(self):
        return Friends.objects.get_or_create(user=self.request.user)[0]


class FriendsList(ListAPIView):
    """Endpoint returns friends list for requesting user.

    Returns requested page of users ordered by
    username ascending.
    """

    serializer_class = FriendsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.friends_list.all().order_by("username")
