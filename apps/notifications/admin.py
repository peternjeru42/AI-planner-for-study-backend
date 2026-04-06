from django.contrib import admin

from apps.notifications.models import Notification, NotificationLog


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "notification_type", "channel", "status", "created_at")
    list_filter = ("notification_type", "channel", "status")


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("notification", "action", "timestamp")

# Register your models here.
