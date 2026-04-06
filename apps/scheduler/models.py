from django.conf import settings
from django.db import models

from common.constants import JOB_STATUS_CHOICES
from common.mixins import TimeStampedMixin, UUIDPrimaryKeyMixin


class ScheduledJob(UUIDPrimaryKeyMixin, TimeStampedMixin):
    name = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default="queued")
    scheduled_time = models.DateTimeField()
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="scheduled_jobs")
    payload_json = models.JSONField(blank=True, null=True)
    result_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-scheduled_time"]


class JobRunHistory(UUIDPrimaryKeyMixin):
    scheduled_job = models.ForeignKey("scheduler.ScheduledJob", on_delete=models.CASCADE, related_name="run_history")
    run_status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES)
    run_started_at = models.DateTimeField()
    run_ended_at = models.DateTimeField(blank=True, null=True)
    output_log = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

# Create your models here.
