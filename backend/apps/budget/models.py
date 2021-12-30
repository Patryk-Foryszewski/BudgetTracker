from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL


class TimeStamps(models.Model):
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class BaseMixin(TimeStamps):
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


class Income(BaseMixin):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    content = models.TextField(blank=True, default="")
    value = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    budget = models.OneToOneField(
        Budget, related_name="income", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.value}, {self.modified_date}, {self.creator}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Expense(BaseMixin):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    content = models.TextField(blank=True, default="")
    value = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    budget = models.ForeignKey(
        Budget, related_name="expenses", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"Expense {self.name}, {self.creator}, {self.value}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def has_access(self):
        creator_or_participant = Budget.objects.filter(
            Q(pk=self.budget_id)
            & (Q(creator=self.creator_id) | Q(participants=self.creator_id))
        ).first()
        print("HAS ACCESS 1 |", vars(self))
        if not creator_or_participant:
            raise PermissionDenied(
                "User not allowed to create expenses for this budget"
            )
        print(
            "BC or EC",
            self.creator,
            "|",
            self.creator.id,
            "|",
            creator_or_participant.creator.id,
            "|",
            self.creator_id,
        )
        if self.creator and (
            self.creator.id != self.creator_id
            or creator_or_participant.creator.id != self.creator_id
        ):
            raise PermissionDenied(
                "Only Budget Creator or Expense Creator can edit Expense"
            )
