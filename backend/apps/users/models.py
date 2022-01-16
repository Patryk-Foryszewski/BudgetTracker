from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            registered_at=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        is_superuser = extra_fields.pop("is_superuser", False)
        return self._create_user(
            email, password, is_staff, is_superuser, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="Username", default="", max_length=50)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255)
    avatar = models.ImageField(verbose_name="Avatar", blank=True)
    token = models.UUIDField(verbose_name="Token", default=uuid4, editable=False)

    is_admin = models.BooleanField(verbose_name="Admin", default=False)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    is_staff = models.BooleanField(verbose_name="Staff", default=False)
    registered_at = models.DateTimeField(
        verbose_name="Registered at", auto_now_add=timezone.now
    )

    # Fields settings
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @classmethod
    def from_db(cls, db, field_names, values):
        user = super().from_db(db, field_names, values)
        if not user.avatar:
            user.avatar = str(
                settings.MEDIA_ROOT / "defaults/images/default_avatar.png"
            )
        return user
