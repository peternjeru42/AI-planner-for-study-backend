from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from apps.notifications.models import Notification, NotificationLog
from apps.notifications.serializers import NotificationLogSerializer, NotificationSerializer
from apps.notifications.services import NotificationService
from common.permissions import IsAdmin, IsStudent
from common.utils import api_success


class NotificationListView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        queryset = Notification.objects.filter(user=request.user).order_by("-created_at")
        return api_success(NotificationSerializer(queryset, many=True).data, "Notifications fetched successfully.")


class NotificationUnreadCountView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        unread_count = Notification.objects.filter(user=request.user, read_at__isnull=True).exclude(status="read").count()
        return api_success({"count": unread_count}, "Unread notification count fetched successfully.")


class NotificationReadView(APIView):
    permission_classes = [IsStudent]

    def patch(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification = NotificationService.mark_as_read(notification)
        return api_success(NotificationSerializer(notification).data, "Notification marked as read successfully.")


class NotificationTriggerSimulatedView(APIView):
    permission_classes = [IsStudent]

    def post(self, request):
        notifications = NotificationService.trigger_due_notifications(request.user)
        return api_success(NotificationSerializer(notifications, many=True).data, "Simulated notifications triggered successfully.", 201)


class NotificationLogListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = NotificationLog.objects.select_related("notification").all()
        paginator = Paginator(queryset, int(request.query_params.get("pageSize", 20)))
        page = paginator.get_page(request.query_params.get("page", 1))
        return api_success(
            {
                "results": NotificationLogSerializer(page.object_list, many=True).data,
                "count": paginator.count,
                "numPages": paginator.num_pages,
                "page": page.number,
            },
            "Notification logs fetched successfully.",
        )

# Create your views here.
