from datetime import time

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from common.constants import USER_ROLE_CHOICES
from common.mixins import TimeStampedMixin, UUIDPrimaryKeyMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        return self.create_user(email, password, **extra_fields)


class User(UUIDPrimaryKeyMixin, AbstractBaseUser, PermissionsMixin, TimeStampedMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default="student")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class StudentProfile(UUIDPrimaryKeyMixin, TimeStampedMixin):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="student_profile")
    course_name = models.CharField(max_length=255, blank=True)
    year_of_study = models.PositiveIntegerField(default=1)
    institution_name = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    preferred_study_start_time = models.TimeField(default=time(8, 0))
    preferred_study_end_time = models.TimeField(default=time(22, 0))
    preferred_session_length_minutes = models.PositiveIntegerField(default=60)
    preferred_break_length_minutes = models.PositiveIntegerField(default=15)
    max_sessions_per_day = models.PositiveIntegerField(default=6)
    weekend_available = models.BooleanField(default=True)
    enable_in_app_notifications = models.BooleanField(default=True)
    enable_email_notifications_simulated = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} profile"

# Create your models here.
