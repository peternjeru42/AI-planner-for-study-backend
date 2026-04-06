from rest_framework import serializers

from apps.assessments.models import Assessment
from common.utils import snake_to_frontend


class AssessmentSerializer(serializers.ModelSerializer):
    userId = serializers.UUIDField(source="user_id", read_only=True)
    subjectId = serializers.UUIDField(source="subject_id")
    type = serializers.CharField(source="assessment_type")
    dueDate = serializers.DateField(source="due_date", format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    dueTime = serializers.TimeField(source="due_time", format="%H:%M", required=False, allow_null=True, input_formats=["%H:%M"])
    weight = serializers.IntegerField(source="weight_percentage")
    estimatedHours = serializers.DecimalField(source="estimated_hours", max_digits=6, decimal_places=2)
    priority = serializers.CharField(source="manual_priority", required=False, allow_blank=True)
    calculatedPriorityScore = serializers.FloatField(source="calculated_priority_score", read_only=True)
    lockedAfterCompletion = serializers.BooleanField(source="is_locked_after_completion", required=False)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = [
            "id",
            "userId",
            "subjectId",
            "title",
            "type",
            "dueDate",
            "dueTime",
            "weight",
            "estimatedHours",
            "priority",
            "notes",
            "status",
            "calculatedPriorityScore",
            "lockedAfterCompletion",
            "createdAt",
            "updatedAt",
        ]

    def get_status(self, obj):
        return snake_to_frontend(obj.status)

    def create(self, validated_data):
        return Assessment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AssessmentStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["pending", "in-progress", "completed", "missed", "overdue"])


class FilterOptionsSerializer(serializers.Serializer):
    types = serializers.ListField(child=serializers.CharField())
    statuses = serializers.ListField(child=serializers.CharField())
