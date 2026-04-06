from django.contrib import admin

from apps.assessments.models import Assessment


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("title", "assessment_type", "subject", "user", "due_date", "status")
    search_fields = ("title", "subject__name", "user__email")
    list_filter = ("assessment_type", "status", "due_date")

# Register your models here.
