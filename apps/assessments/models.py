from django.conf import settings
from django.db import models

from common.constants import ASSESSMENT_STATUS_CHOICES, ASSESSMENT_TYPE_CHOICES
from common.mixins import TimeStampedMixin, UUIDPrimaryKeyMixin


class Assessment(UUIDPrimaryKeyMixin, TimeStampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assessments")
    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE, related_name="assessments")
    title = models.CharField(max_length=255)
    assessment_type = models.CharField(max_length=32, choices=ASSESSMENT_TYPE_CHOICES)
    due_date = models.DateField()
    due_time = models.TimeField(blank=True, null=True)
    weight_percentage = models.PositiveIntegerField(default=0)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    manual_priority = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ASSESSMENT_STATUS_CHOICES, default="pending")
    calculated_priority_score = models.FloatField(default=0)
    is_locked_after_completion = models.BooleanField(default=False)

    class Meta:
        ordering = ["due_date", "due_time", "created_at"]

    def __str__(self):
        return self.title

# Create your models here.
