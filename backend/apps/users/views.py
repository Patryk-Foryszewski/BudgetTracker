from apps.users.models import Friends, User
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    FriendsAddSerializer,
    FriendsSerializer,
    UserListSerializer,
    UserSerializer,
)


class UserProfile(RetrieveAPIView):
    """Use this view to check user profile."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UsersList(ListAPIView):
    """
    Use this view to search users

    filters by below fields
    username; contains
    email; exact

    usage exapmles:
    {
    "search": "user@example.com"
    }


    """

    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    # filter_backends = UserFilter
    paginate_by = 40

    def get_queryset(self):
        value = self.kwargs["search"]
        queryset = User.objects.filter(
            Q(username__icontains=value) | Q(email__exact=value)
        )
        return queryset.order_by("-post_time")


class FriendsAdd(UpdateAPIView):
    model = Friends
    queryset = Friends.objects.all()
    serializer_class = FriendsAddSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Friends.objects.get_or_create(user=self.request.user)[0]


class FriendsList(ListAPIView):
    serializer_class = FriendsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.friends_list.all()
