from django.conf import settings
from django.db import models

from common.mixins import UUIDPrimaryKeyMixin


class WeeklyMetricsSnapshot(UUIDPrimaryKeyMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weekly_metric_snapshots")
    week_start = models.DateField()
    tasks_completed = models.PositiveIntegerField(default=0)
    study_minutes_completed = models.PositiveIntegerField(default=0)
    study_minutes_planned = models.PositiveIntegerField(default=0)
    completion_rate = models.FloatField(default=0)
    overdue_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-week_start"]

# Create your models here.
