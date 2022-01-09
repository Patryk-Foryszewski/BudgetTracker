from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Friends
from .serializers import FriendsAddSerializer, FriendsSerializer

User = get_user_model()


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
