from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from applications.models import InternshipApplication
from internships.models import InternshipListing
from notifications.utils import create_notification
from users.models import UserProfile


@shared_task
def close_expired_internships():
    today = timezone.localdate()
    updated = InternshipListing.objects.filter(
        application_deadline__lt=today,
        status=InternshipListing.Status.APPROVED,
    ).update(status=InternshipListing.Status.CLOSED)
    return updated


@shared_task
def send_weekly_log_reminders():
    students = get_user_model().objects.filter(
        userprofile__role=UserProfile.Role.STUDENT,
        studentprofile__applications__status=InternshipApplication.Status.ACCEPTED,
    ).distinct()
    for user in students:
        create_notification(
            user,
            "Weekly log reminder",
            "Please submit your internship weekly progress log.",
            send_email=True,
        )
    return students.count()


@shared_task
def send_interview_reminders():
    upcoming = InternshipApplication.objects.filter(
        interview_date__date=timezone.localdate() + timezone.timedelta(days=1)
    ).select_related("student__user", "internship")
    for application in upcoming:
        create_notification(
            application.student.user,
            "Interview reminder",
            f"Your interview for {application.internship.title} is scheduled tomorrow.",
            send_email=True,
        )
    return upcoming.count()
