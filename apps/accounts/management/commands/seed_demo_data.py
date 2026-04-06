from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import StudentProfile, User
from apps.assessments.models import Assessment
from apps.notifications.services import NotificationService
from apps.planner.models import StudyPlan
from apps.planner.services import PlannerService
from apps.progress.services import ProgressService
from apps.scheduler.services import SchedulerService
from apps.subjects.models import Subject


class Command(BaseCommand):
    help = "Seed demo StudyFlow data for local development."

    def handle(self, *args, **options):
        admin_user, _ = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "full_name": "Dr. Sarah Mitchell",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
                "is_verified": True,
            },
        )
        admin_user.set_password("demo123")
        admin_user.save()

        student_user, created = User.objects.get_or_create(
            email="student@example.com",
            defaults={
                "full_name": "Alex Johnson",
                "role": "student",
                "is_verified": True,
            },
        )
        student_user.set_password("demo123")
        student_user.save()

        StudentProfile.objects.update_or_create(
            user=student_user,
            defaults={
                "course_name": "Computer Science",
                "year_of_study": 2,
                "institution_name": "StudyFlow University",
                "timezone": "Africa/Nairobi",
                "preferred_session_length_minutes": 60,
                "preferred_break_length_minutes": 15,
                "max_sessions_per_day": 6,
                "weekend_available": True,
            },
        )

        student_user.subjects.all().delete()
        colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]
        subject_specs = [
            ("Data Structures & Algorithms", "CS201", "Prof. James Chen"),
            ("Web Development", "CS301", "Prof. Emily Rodriguez"),
            ("Advanced Mathematics", "MATH301", "Prof. Robert Kumar"),
        ]
        subjects = []
        for index, (name, code, instructor) in enumerate(subject_specs):
            subjects.append(
                Subject.objects.create(
                    user=student_user,
                    name=name,
                    code=code,
                    instructor_name=instructor,
                    semester="Spring 2026",
                    color_tag=colors[index],
                    description=f"Demo subject for {name}.",
                )
            )

        today = timezone.localdate()
        assessment_specs = [
            (subjects[0], "Binary Tree Implementation Project", "assignment", 7, "23:59", 15, 6, "high"),
            (subjects[0], "Midterm Exam - Data Structures", "exam", 14, "10:00", 30, 20, "high"),
            (subjects[1], "React Dashboard Application", "project", 10, "23:59", 25, 12, "high"),
            (subjects[2], "Linear Algebra CAT", "cat", 5, "14:00", 20, 8, "medium"),
        ]
        for subject, title, assessment_type, days_out, due_time, weight, hours, priority in assessment_specs:
            Assessment.objects.create(
                user=student_user,
                subject=subject,
                title=title,
                assessment_type=assessment_type,
                due_date=today + timedelta(days=days_out),
                due_time=timezone.datetime.strptime(due_time, "%H:%M").time(),
                weight_percentage=weight,
                estimated_hours=hours,
                manual_priority=priority,
                status="pending",
            )

        StudyPlan.objects.filter(user=student_user).delete()
        plan, sessions = PlannerService.generate_plan(user=student_user, trigger="manual")
        NotificationService.trigger_due_notifications(student_user)
        ProgressService.sync_all_subject_progress(student_user)
        SchedulerService.simulate_cycle()

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data seeded. Admin=admin@example.com/demo123, Student=student@example.com/demo123, plan={plan.id}, sessions={len(sessions)}"
            )
        )
