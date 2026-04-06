from rest_framework import serializers

from apps.scheduler.models import JobRunHistory, ScheduledJob


class JobRunHistorySerializer(serializers.ModelSerializer):
    taskId = serializers.UUIDField(source="scheduled_job_id")
    startTime = serializers.DateTimeField(source="run_started_at")
    endTime = serializers.DateTimeField(source="run_ended_at", allow_null=True)
    status = serializers.CharField(source="run_status")
    result = serializers.CharField(source="output_log")

    class Meta:
        model = JobRunHistory
        fields = ["id", "taskId", "startTime", "endTime", "status", "result"]


class ScheduledJobSerializer(serializers.ModelSerializer):
    lastRunTime = serializers.SerializerMethodField()
    nextRunTime = serializers.DateTimeField(source="scheduled_time")
    runHistory = JobRunHistorySerializer(source="run_history", many=True, read_only=True)

    class Meta:
        model = ScheduledJob
        fields = ["id", "name", "status", "lastRunTime", "nextRunTime", "runHistory"]

    def get_lastRunTime(self, obj):
        run = obj.run_history.order_by("-run_started_at").first()
        return run.run_started_at if run else None


class RunJobSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    jobType = serializers.CharField(required=False, allow_blank=True)
    targetUserId = serializers.UUIDField(required=False)
