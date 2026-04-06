from django.conf import settings
from django.db import models

from common.constants import NOTIFICATION_CHANNEL_CHOICES, NOTIFICATION_STATUS_CHOICES, NOTIFICATION_TYPE_CHOICES
from common.mixins import TimeStampedMixin, UUIDPrimaryKeyMixin


class Notification(UUIDPrimaryKeyMixin, TimeStampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    subject = models.ForeignKey("subjects.Subject", on_delete=models.SET_NULL, blank=True, null=True, related_name="notifications")
    assessment = models.ForeignKey("assessments.Assessment", on_delete=models.SET_NULL, blank=True, null=True, related_name="notifications")
    study_session = models.ForeignKey("planner.StudySession", on_delete=models.SET_NULL, blank=True, null=True, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=40, choices=NOTIFICATION_TYPE_CHOICES)
    channel = models.CharField(max_length=20, choices=NOTIFICATION_CHANNEL_CHOICES, default="in_app")
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS_CHOICES, default="queued")
    scheduled_for = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    is_simulated = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]


class NotificationLog(UUIDPrimaryKeyMixin):
    notification = models.ForeignKey("notifications.Notification", on_delete=models.CASCADE, related_name="logs")
    action = models.CharField(max_length=30)
    detail = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

# Create your models here.
