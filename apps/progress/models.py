from django.conf import settings
from django.db import models

from common.mixins import UUIDPrimaryKeyMixin


class AssessmentProgress(UUIDPrimaryKeyMixin):
    assessment = models.OneToOneField("assessments.Assessment", on_delete=models.CASCADE, related_name="progress_record")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assessment_progress_records")
    progress_percent = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="pending")
    last_updated_at = models.DateTimeField(auto_now=True)


class StudySessionCompletion(UUIDPrimaryKeyMixin):
    study_session = models.OneToOneField("planner.StudySession", on_delete=models.CASCADE, related_name="completion_record")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_session_completion_records")
    completed_at = models.DateTimeField(blank=True, null=True)
    actual_minutes = models.PositiveIntegerField(blank=True, null=True)
    completion_status = models.CharField(max_length=20, default="planned")
    remarks = models.TextField(blank=True)


class SubjectProgress(UUIDPrimaryKeyMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subject_progress_records")
    subject = models.OneToOneField("subjects.Subject", on_delete=models.CASCADE, related_name="progress_record")
    total_assessments = models.PositiveIntegerField(default=0)
    completed_assessments = models.PositiveIntegerField(default=0)
    total_planned_minutes = models.PositiveIntegerField(default=0)
    total_completed_minutes = models.PositiveIntegerField(default=0)
    completion_rate = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
