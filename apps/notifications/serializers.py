from rest_framework import serializers

from apps.notifications.models import Notification, NotificationLog
from common.utils import snake_to_frontend


class NotificationSerializer(serializers.ModelSerializer):
    userId = serializers.UUIDField(source="user_id", read_only=True)
    type = serializers.SerializerMethodField()
    channel = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source="created_at")
    sentAt = serializers.DateTimeField(source="sent_at", allow_null=True)
    read = serializers.SerializerMethodField()
    readAt = serializers.DateTimeField(source="read_at", allow_null=True)
    relatedAssessmentId = serializers.UUIDField(source="assessment_id", allow_null=True)
    isSimulated = serializers.BooleanField(source="is_simulated")

    class Meta:
        model = Notification
        fields = [
            "id",
            "userId",
            "title",
            "message",
            "type",
            "channel",
            "status",
            "createdAt",
            "sentAt",
            "read",
            "readAt",
            "relatedAssessmentId",
            "isSimulated",
        ]

    def get_type(self, obj):
        return snake_to_frontend(obj.notification_type)

    def get_channel(self, obj):
        return snake_to_frontend(obj.channel)

    def get_read(self, obj):
        return obj.read_at is not None or obj.status == "read"


class NotificationLogSerializer(serializers.ModelSerializer):
    notificationId = serializers.UUIDField(source="notification_id")
    timestamp = serializers.DateTimeField()

    class Meta:
        model = NotificationLog
        fields = ["id", "notificationId", "action", "detail", "timestamp"]
