from django.contrib import admin

from apps.reports.models import WeeklyMetricsSnapshot


@admin.register(WeeklyMetricsSnapshot)
class WeeklyMetricsSnapshotAdmin(admin.ModelAdmin):
    list_display = ("user", "week_start", "tasks_completed", "completion_rate", "overdue_count")

# Register your models here.
