from django.urls import path

from apps.calendar_app.views import CalendarDayView, CalendarEventsView, CalendarMonthView, CalendarWeekView


urlpatterns = [
    path("events/", CalendarEventsView.as_view(), name="calendar-events"),
    path("month/", CalendarMonthView.as_view(), name="calendar-month"),
    path("week/", CalendarWeekView.as_view(), name="calendar-week"),
    path("day/", CalendarDayView.as_view(), name="calendar-day"),
]
