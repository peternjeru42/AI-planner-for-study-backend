from django.urls import path

from apps.notifications.views import (
    NotificationListView,
    NotificationLogListView,
    NotificationReadView,
    NotificationTriggerSimulatedView,
    NotificationUnreadCountView,
)


urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("unread-count/", NotificationUnreadCountView.as_view(), name="notification-unread-count"),
    path("<uuid:notification_id>/read/", NotificationReadView.as_view(), name="notification-read"),
    path("trigger-simulated/", NotificationTriggerSimulatedView.as_view(), name="notification-trigger-simulated"),
    path("logs/", NotificationLogListView.as_view(), name="notification-logs"),
]
