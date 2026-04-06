from django.contrib import admin

from apps.scheduler.models import JobRunHistory, ScheduledJob


@admin.register(ScheduledJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ("name", "job_type", "status", "scheduled_time", "target_user")


@admin.register(JobRunHistory)
class JobRunHistoryAdmin(admin.ModelAdmin):
    list_display = ("scheduled_job", "run_status", "run_started_at", "run_ended_at")

# Register your models here.
