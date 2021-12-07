from apps.users.models import User
from django.db import models


class TimeStamps(models.Model):
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class BaseMixin(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Budget(BaseMixin):
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.PROTECT)
    participants = models.ManyToManyField(User, related_name="participants")
    name = models.CharField(max_length=30)
    content = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Name: {self.name}, Creator {self.creator}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
