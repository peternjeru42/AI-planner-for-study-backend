from rest_framework.decorators import action

from apps.assessments.models import Assessment
from apps.assessments.serializers import AssessmentSerializer, AssessmentStatusSerializer, FilterOptionsSerializer
from apps.assessments.services import AssessmentService
from apps.progress.services import ProgressService
from common.permissions import IsStudent
from common.utils import api_success
from common.viewsets import EnvelopedModelViewSet


class AssessmentViewSet(EnvelopedModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsStudent]
    pagination_class = None
    filterset_fields = []
    search_fields = ["title"]
    ordering_fields = ["due_date", "weight_percentage", "created_at", "calculated_priority_score"]
    success_messages = {
        **EnvelopedModelViewSet.success_messages,
        "list": "Assessments fetched successfully.",
        "create": "Assessment created successfully.",
        "update": "Assessment updated successfully.",
        "destroy": "Assessment deleted successfully.",
    }

    def get_queryset(self):
        queryset = Assessment.objects.filter(user=self.request.user).select_related("subject")
        AssessmentService.update_overdue_items(queryset)
        params = self.request.query_params
        if params.get("subject"):
            queryset = queryset.filter(subject_id=params["subject"])
        if params.get("type"):
            queryset = queryset.filter(assessment_type=params["type"])
        if params.get("status"):
            queryset = queryset.filter(status=params["status"].replace("-", "_"))
        if params.get("due_from"):
            queryset = queryset.filter(due_date__gte=params["due_from"])
        if params.get("due_to"):
            queryset = queryset.filter(due_date__lte=params["due_to"])
        ordering = params.get("ordering")
        if ordering:
            queryset = queryset.order_by(ordering.replace("dueDate", "due_date"))
        return queryset

    def perform_create(self, serializer):
        assessment = serializer.save(user=self.request.user)
        AssessmentService.refresh_assessment(assessment)
        ProgressService.sync_subject_progress_for_subject(assessment.subject)

    def perform_update(self, serializer):
        assessment = serializer.save()
        AssessmentService.refresh_assessment(assessment)
        ProgressService.sync_subject_progress_for_subject(assessment.subject)

    @action(detail=True, methods=["patch"], url_path="status")
    def patch_status(self, request, pk=None):
        assessment = self.get_object()
        serializer = AssessmentStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assessment.status = serializer.validated_data["status"].replace("-", "_")
        if assessment.status == "completed":
            assessment.is_locked_after_completion = True
        AssessmentService.refresh_assessment(assessment)
        ProgressService.sync_subject_progress_for_subject(assessment.subject)
        return api_success(AssessmentSerializer(assessment).data, "Assessment status updated successfully.")

    @action(detail=False, methods=["get"], url_path="upcoming")
    def upcoming(self, request):
        queryset = self.get_queryset().filter(status__in=["pending", "in_progress", "overdue"]).order_by("due_date")[:10]
        return api_success(AssessmentSerializer(queryset, many=True).data, "Upcoming assessments fetched successfully.")

    @action(detail=False, methods=["get"], url_path="overdue")
    def overdue(self, request):
        queryset = self.get_queryset().filter(status="overdue")
        return api_success(AssessmentSerializer(queryset, many=True).data, "Overdue assessments fetched successfully.")

    @action(detail=False, methods=["get"], url_path="filter-options")
    def filter_options(self, request):
        serializer = FilterOptionsSerializer(AssessmentService.filter_options())
        return api_success(serializer.data, "Assessment filter options fetched successfully.")

# Create your views here.
