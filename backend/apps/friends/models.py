from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Friends(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friends")
    friends_list = models.ManyToManyField(User, related_name="friends_list", blank=True)

    def __str__(self):
        return self.user.username
