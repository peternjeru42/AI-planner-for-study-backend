from django.conf import settings
from django.db import models

from common.constants import PLAN_STATUS_CHOICES, PLAN_TRIGGER_CHOICES, SESSION_STATUS_CHOICES, SESSION_TYPE_CHOICES
from common.mixins import TimeStampedMixin, UUIDPrimaryKeyMixin


class StudyPlan(UUIDPrimaryKeyMixin, TimeStampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_plans")
    title = models.CharField(max_length=255)
    generated_for_start_date = models.DateField()
    generated_for_end_date = models.DateField()
    generation_trigger = models.CharField(max_length=40, choices=PLAN_TRIGGER_CHOICES, default="manual")
    status = models.CharField(max_length=20, choices=PLAN_STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class StudySession(UUIDPrimaryKeyMixin, TimeStampedMixin):
    study_plan = models.ForeignKey("planner.StudyPlan", on_delete=models.CASCADE, related_name="sessions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_sessions")
    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE, related_name="study_sessions")
    assessment = models.ForeignKey("assessments.Assessment", on_delete=models.SET_NULL, blank=True, null=True, related_name="study_sessions")
    title = models.CharField(max_length=255)
    session_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    session_type = models.CharField(max_length=32, choices=SESSION_TYPE_CHOICES, default="revision")
    priority_score = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default="planned")
    notes = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ["session_date", "start_time"]

    def __str__(self):
        return self.title


class PlannerLog(UUIDPrimaryKeyMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="planner_logs")
    study_plan = models.ForeignKey("planner.StudyPlan", on_delete=models.SET_NULL, blank=True, null=True, related_name="logs")
    trigger_source = models.CharField(max_length=40)
    input_snapshot_json = models.JSONField(default=dict)
    output_snapshot_json = models.JSONField(default=dict)
    status = models.CharField(max_length=30)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

# Create your models here.
