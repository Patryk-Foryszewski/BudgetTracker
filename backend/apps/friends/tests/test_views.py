import json

from apps.budget.tests.utils import request_factory
from apps.users.tests.factories import UserFactory
from django.test import TestCase
from rest_framework import status
from rest_framework.test import force_authenticate

from ..models import Friends
from ..views import FriendsAdd, FriendsList, FriendsRemove


class AddFriends(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.user = UserFactory()
        cls.friend_1 = UserFactory()
        cls.friend_2 = UserFactory()

    def test_unauthenticated_user(self):
        request = request_factory.patch("/")
        response = FriendsAdd.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_two_friends_one_by_one(self):
        data = json.dumps({"friends_list": [self.friend_1.pk]})
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = FriendsAdd.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.dumps({"friends_list": [self.friend_2.pk]})
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = FriendsAdd.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(self.user.friends.friends_list.all()))

    def test_add_two_friends_at_a_time(self):
        data = json.dumps({"friends_list": [self.friend_1.pk, self.friend_2.pk]})
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = FriendsAdd.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(self.user.friends.friends_list.all()))


class RemoveFriend(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.friend_1 = UserFactory()
        cls.friend_2 = UserFactory()
        cls.friends = Friends.objects.create(user=cls.user)
        cls.friends.friends_list.set([cls.friend_1, cls.friend_2])

    def test_unauthenticated_user(self):
        request = request_factory.patch("/")
        response = FriendsRemove.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_friend(self):
        data = json.dumps({"friends_list": [self.friend_1.pk]})
        request = request_factory.patch("/", data=data, content_type="application/json")
        force_authenticate(request, user=self.user)
        response = FriendsRemove.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(self.friends.friends_list.all()))


class ListFriends(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.friend_1 = UserFactory()
        cls.friend_2 = UserFactory()
        cls.friend_3 = UserFactory()
        cls.friends = Friends.objects.create(user=cls.user)
        cls.friends_list = [cls.friend_1, cls.friend_2, cls.friend_3]
        cls.friends.friends_list.set(cls.friends_list)

    def test_friend_list(self):
        request = request_factory.get("/")
        force_authenticate(request, user=self.user)
        response = FriendsList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.friends_list))
