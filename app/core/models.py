"""
Database models.
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Event(models.Model):
    """Event object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    date = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    maximum_capacity = models.IntegerField()
    total_booking = models.IntegerField(default=0)
    link = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, default="India")
    MODE_OF_EVENT = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )
    mode = models.CharField(
        max_length=10,
        choices=MODE_OF_EVENT,
        default='online'
    )

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Booking object."""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )
    event_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()

