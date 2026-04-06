from rest_framework import serializers

from apps.progress.models import SubjectProgress


class SubjectProgressSerializer(serializers.ModelSerializer):
    userId = serializers.UUIDField(source="user_id", read_only=True)
    subjectId = serializers.UUIDField(source="subject_id", read_only=True)
    completedAssignments = serializers.IntegerField(source="completed_assessments")
    totalAssignments = serializers.IntegerField(source="total_assessments")
    completionRate = serializers.FloatField(source="completion_rate")
    studyHours = serializers.SerializerMethodField()
    lastUpdated = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = SubjectProgress
        fields = [
            "userId",
            "subjectId",
            "completedAssignments",
            "totalAssignments",
            "completionRate",
            "studyHours",
            "lastUpdated",
        ]

    def get_studyHours(self, obj):
        return round(obj.total_completed_minutes / 60, 2)
