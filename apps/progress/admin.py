from django.contrib import admin

from apps.progress.models import AssessmentProgress, StudySessionCompletion, SubjectProgress


@admin.register(AssessmentProgress)
class AssessmentProgressAdmin(admin.ModelAdmin):
    list_display = ("assessment", "user", "progress_percent", "status", "last_updated_at")


@admin.register(StudySessionCompletion)
class StudySessionCompletionAdmin(admin.ModelAdmin):
    list_display = ("study_session", "user", "completion_status", "actual_minutes", "completed_at")


@admin.register(SubjectProgress)
class SubjectProgressAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "completion_rate", "total_completed_minutes", "updated_at")

# Register your models here.
