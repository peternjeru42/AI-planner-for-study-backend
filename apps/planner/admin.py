from django.contrib import admin

from apps.planner.models import PlannerLog, StudyPlan, StudySession


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "generation_trigger", "generated_for_start_date", "generated_for_end_date")


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "session_date", "start_time", "end_time", "status")
    list_filter = ("status", "session_date")


@admin.register(PlannerLog)
class PlannerLogAdmin(admin.ModelAdmin):
    list_display = ("trigger_source", "user", "study_plan", "status", "created_at")

# Register your models here.
