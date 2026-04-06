from django.contrib import admin

from apps.subjects.models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "user", "semester", "is_active")
    search_fields = ("name", "code", "user__email")
    list_filter = ("is_active", "semester")

# Register your models here.
