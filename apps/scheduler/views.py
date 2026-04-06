from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.scheduler.models import JobRunHistory, ScheduledJob
from apps.scheduler.serializers import JobRunHistorySerializer, RunJobSerializer, ScheduledJobSerializer
from apps.scheduler.services import SchedulerService
from common.permissions import IsAdmin
from common.utils import api_success


class SchedulerJobListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = ScheduledJob.objects.prefetch_related("run_history").all()
        return api_success(ScheduledJobSerializer(queryset, many=True).data, "Scheduled jobs fetched successfully.")


class SchedulerRunJobView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = RunJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_user = None
        if serializer.validated_data.get("targetUserId"):
            target_user = get_object_or_404(User, id=serializer.validated_data["targetUserId"])
        job = SchedulerService.create_job(
            name=serializer.validated_data.get("name") or "manual_run",
            job_type=serializer.validated_data.get("jobType") or "manual",
            target_user=target_user,
            payload=request.data,
        )
        SchedulerService.run_job(job)
        return api_success(ScheduledJobSerializer(job).data, "Scheduled job executed successfully.", 201)


class SchedulerHistoryView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = JobRunHistory.objects.select_related("scheduled_job").all()
        paginator = Paginator(queryset, int(request.query_params.get("pageSize", 20)))
        page = paginator.get_page(request.query_params.get("page", 1))
        return api_success(
            {
                "results": JobRunHistorySerializer(page.object_list, many=True).data,
                "count": paginator.count,
                "numPages": paginator.num_pages,
                "page": page.number,
            },
            "Scheduler history fetched successfully.",
        )


class SchedulerSimulateCycleView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        jobs = SchedulerService.simulate_cycle()
        return api_success(ScheduledJobSerializer(jobs, many=True).data, "Scheduler cycle simulated successfully.", 201)

# Create your views here.
