ASSESSMENT_TYPE_CHOICES = (
    ("assignment", "Assignment"),
    ("cat", "CAT"),
    ("quiz", "Quiz"),
    ("exam", "Exam"),
    ("project", "Project"),
    ("presentation", "Presentation"),
)

ASSESSMENT_STATUS_CHOICES = (
    ("pending", "Pending"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("missed", "Missed"),
    ("overdue", "Overdue"),
)

PLAN_STATUS_CHOICES = (
    ("draft", "Draft"),
    ("active", "Active"),
    ("archived", "Archived"),
)

PLAN_TRIGGER_CHOICES = (
    ("manual", "Manual"),
    ("assessment_created", "Assessment Created"),
    ("assessment_updated", "Assessment Updated"),
    ("scheduler", "Scheduler"),
    ("preferences_changed", "Preferences Changed"),
)

SESSION_TYPE_CHOICES = (
    ("reading", "Reading"),
    ("revision", "Revision"),
    ("assignment_work", "Assignment Work"),
    ("exam_prep", "Exam Prep"),
    ("project_work", "Project Work"),
)

SESSION_STATUS_CHOICES = (
    ("planned", "Planned"),
    ("completed", "Completed"),
    ("missed", "Missed"),
    ("skipped", "Skipped"),
    ("rescheduled", "Rescheduled"),
)

NOTIFICATION_TYPE_CHOICES = (
    ("deadline_reminder", "Deadline Reminder"),
    ("study_session_reminder", "Study Session Reminder"),
    ("overdue_alert", "Overdue Alert"),
    ("plan_generated", "Plan Generated"),
    ("weekly_report", "Weekly Report"),
)

NOTIFICATION_CHANNEL_CHOICES = (
    ("in_app", "In-App"),
    ("email", "Email"),
)

NOTIFICATION_STATUS_CHOICES = (
    ("queued", "Queued"),
    ("sent", "Sent"),
    ("read", "Read"),
    ("failed", "Failed"),
)

JOB_STATUS_CHOICES = (
    ("queued", "Queued"),
    ("running", "Running"),
    ("completed", "Completed"),
    ("failed", "Failed"),
)

USER_ROLE_CHOICES = (
    ("student", "Student"),
    ("admin", "Admin"),
)
