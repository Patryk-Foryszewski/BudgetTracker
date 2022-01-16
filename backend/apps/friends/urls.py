from django.urls import path

from .views import FriendsAdd, FriendsList, FriendsRemove

urlpatterns = [
    path("add_friend/", FriendsAdd.as_view(), name="add_friend"),
    path("remove_friend/", FriendsRemove.as_view(), name="remove_friend"),
    path("friends_list/", FriendsList.as_view(), name="friends_list"),
]
