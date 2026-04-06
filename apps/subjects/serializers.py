from rest_framework import serializers

from apps.subjects.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    userId = serializers.UUIDField(source="user_id", read_only=True)
    instructor = serializers.CharField(source="instructor_name", allow_blank=True, required=False)
    color = serializers.CharField(source="color_tag", required=False)
    isActive = serializers.BooleanField(source="is_active", required=False)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Subject
        fields = [
            "id",
            "userId",
            "name",
            "code",
            "instructor",
            "semester",
            "color",
            "description",
            "isActive",
            "createdAt",
            "updatedAt",
        ]


class SubjectProgressSnapshotSerializer(serializers.Serializer):
    subjectId = serializers.UUIDField()
    totalAssessments = serializers.IntegerField()
    completedAssessments = serializers.IntegerField()
    completionRate = serializers.FloatField()
    studyHours = serializers.FloatField()
