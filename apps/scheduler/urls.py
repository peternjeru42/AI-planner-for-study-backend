from django.urls import path

from apps.scheduler.views import SchedulerHistoryView, SchedulerJobListView, SchedulerRunJobView, SchedulerSimulateCycleView


urlpatterns = [
    path("jobs/", SchedulerJobListView.as_view(), name="scheduler-jobs"),
    path("jobs/run/", SchedulerRunJobView.as_view(), name="scheduler-jobs-run"),
    path("history/", SchedulerHistoryView.as_view(), name="scheduler-history"),
    path("simulate-cycle/", SchedulerSimulateCycleView.as_view(), name="scheduler-simulate-cycle"),
]
