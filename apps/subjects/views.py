from rest_framework.decorators import action

from apps.subjects.models import Subject
from apps.subjects.serializers import SubjectProgressSnapshotSerializer, SubjectSerializer
from apps.subjects.services import SubjectService
from common.permissions import IsStudent
from common.utils import api_success
from common.viewsets import EnvelopedModelViewSet


class SubjectViewSet(EnvelopedModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsStudent]
    pagination_class = None
    success_messages = {
        **EnvelopedModelViewSet.success_messages,
        "list": "Subjects fetched successfully.",
        "create": "Subject created successfully.",
        "update": "Subject updated successfully.",
        "destroy": "Subject deleted successfully.",
    }

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user).order_by("name")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], url_path="progress")
    def progress(self, request, pk=None):
        subject = self.get_object()
        snapshot = SubjectService.subject_progress(subject)
        serializer = SubjectProgressSnapshotSerializer(snapshot)
        return api_success(serializer.data, "Subject progress fetched successfully.")

# Create your views here.
