from django.utils import timezone

from apps.notifications.models import Notification, NotificationLog


class NotificationService:
    @staticmethod
    def create_notification(
        *,
        user,
        title,
        message,
        notification_type,
        channel="in_app",
        status="queued",
        subject=None,
        assessment=None,
        study_session=None,
        scheduled_for=None,
        is_simulated=False,
    ):
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            channel=channel,
            status=status,
            subject=subject,
            assessment=assessment,
            study_session=study_session,
            scheduled_for=scheduled_for,
            is_simulated=is_simulated,
        )
        NotificationLog.objects.create(notification=notification, action="generated", detail=message)
        return notification

    @staticmethod
    def mark_as_read(notification):
        notification.status = "read"
        notification.read_at = timezone.now()
        notification.save(update_fields=["status", "read_at"])
        NotificationLog.objects.create(notification=notification, action="read", detail="Notification marked as read.")
        return notification

    @staticmethod
    def simulate_email_dispatch(queryset=None):
        queryset = queryset or Notification.objects.filter(channel="email", status="queued")
        updated = []
        for notification in queryset:
            notification.status = "sent"
            notification.sent_at = timezone.now()
            notification.save(update_fields=["status", "sent_at"])
            NotificationLog.objects.create(notification=notification, action="sent", detail="Email sent simulated.")
            updated.append(notification)
        return updated

    @classmethod
    def trigger_due_notifications(cls, user):
        created = []
        assessments = user.assessments.filter(status__in=["pending", "in_progress", "overdue"]).order_by("due_date")[:3]
        for assessment in assessments:
            created.append(
                cls.create_notification(
                    user=user,
                    title="Upcoming deadline",
                    message=f"{assessment.title} is approaching.",
                    notification_type="deadline_reminder",
                    channel="in_app",
                    status="sent",
                    assessment=assessment,
                )
            )
        sessions = user.study_sessions.filter(status="planned").order_by("session_date", "start_time")[:2]
        for session in sessions:
            created.append(
                cls.create_notification(
                    user=user,
                    title="Study session reminder",
                    message=f"You have {session.title} scheduled soon.",
                    notification_type="study_session_reminder",
                    channel="email",
                    status="queued",
                    study_session=session,
                    is_simulated=True,
                )
            )
        cls.simulate_email_dispatch(Notification.objects.filter(id__in=[item.id for item in created], channel="email"))
        return created

    @classmethod
    def plan_generated(cls, user, plan):
        return cls.create_notification(
            user=user,
            title="Plan generated",
            message=f"Your study plan '{plan.title}' is ready.",
            notification_type="plan_generated",
            channel="in_app",
            status="sent",
        )
