from django.contrib import admin

from apps.auditlog.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "target_model", "target_id", "actor_user", "created_at")
    search_fields = ("action", "target_model", "target_id", "detail", "actor_user__email")
    list_filter = ("action", "target_model")

# Register your models here.
