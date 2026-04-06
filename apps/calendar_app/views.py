from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView

from apps.calendar_app.services import CalendarService
from common.permissions import IsStudent
from common.utils import api_success


class BaseCalendarView(APIView):
    permission_classes = [IsStudent]

    def build_payload(self, request, start_date, end_date):
        events = CalendarService.assessment_events(request.user, start_date, end_date) + CalendarService.session_events(request.user, start_date, end_date)
        events.sort(key=lambda item: item["start"])
        return api_success(events, "Calendar events fetched successfully.")


class CalendarEventsView(BaseCalendarView):
    def get(self, request):
        start_date = request.query_params.get("start") or timezone.localdate().isoformat()
        end_date = request.query_params.get("end") or (timezone.localdate() + timedelta(days=30)).isoformat()
        return self.build_payload(request, start_date, end_date)


class CalendarMonthView(BaseCalendarView):
    def get(self, request):
        start = timezone.localdate().replace(day=1)
        end = start + timedelta(days=31)
        return self.build_payload(request, start, end)


class CalendarWeekView(BaseCalendarView):
    def get(self, request):
        start = timezone.localdate()
        end = start + timedelta(days=6)
        return self.build_payload(request, start, end)


class CalendarDayView(BaseCalendarView):
    def get(self, request):
        current = timezone.localdate()
        return self.build_payload(request, current, current)

# Create your views here.
