from django.conf import settings
from django.db import models

from common.mixins import TimeStampedMixin, UUIDPrimaryKeyMixin


class Subject(UUIDPrimaryKeyMixin, TimeStampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    instructor_name = models.CharField(max_length=255, blank=True)
    semester = models.CharField(max_length=100, blank=True)
    color_tag = models.CharField(max_length=20, default="#3B82F6")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("user", "code")

    def __str__(self):
        return f"{self.code} - {self.name}"

# Create your models here.
