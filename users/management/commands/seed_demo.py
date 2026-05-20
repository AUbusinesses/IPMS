from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from applications.models import InternshipApplication, WeeklyLog
from employers.models import EmployerProfile
from internships.models import InternshipListing, Skill
from matching.engine import generate_matches_for_student
from notifications.utils import create_notification
from students.models import StudentProfile
from supervisors.models import Evaluation, SupervisorProfile
from users.models import UserProfile


PASSWORD = "DemoPass123!"


class Command(BaseCommand):
    help = "Create demo accounts and sample internship placement data."

    def handle(self, *args, **options):
        skills = {}
        for name in [
            "Python",
            "Django",
            "JavaScript",
            "SQL",
            "Data Analysis",
            "Cyber Security",
            "Communication",
            "React",
        ]:
            skills[name], _ = Skill.objects.get_or_create(name=name)

        officer = self._user("officer", "Placement", "Officer", "officer@iipms.local")
        self._profile(officer, UserProfile.Role.PLACEMENT_OFFICER, True)

        supervisor_user = self._user("supervisor", "Asha", "Patel", "supervisor@iipms.local")
        self._profile(supervisor_user, UserProfile.Role.SUPERVISOR, True)
        supervisor = SupervisorProfile.objects.get(user=supervisor_user)
        supervisor.department = "ICT"
        supervisor.save()

        employer_user = self._user("employer", "Jordan", "Miles", "employer@iipms.local")
        self._profile(employer_user, UserProfile.Role.EMPLOYER, True)
        employer = EmployerProfile.objects.get(user=employer_user)
        employer.company_name = "Southern Cross Digital"
        employer.industry = "Software Consulting"
        employer.location = "Sydney"
        employer.is_verified = True
        employer.save()

        student_user = self._user("student", "Mia", "Chen", "student@iipms.local")
        self._profile(student_user, UserProfile.Role.STUDENT, True)
        student = StudentProfile.objects.get(user=student_user)
        student.student_id = "ICT802001"
        student.course = "Master of Information Technology"
        student.gpa_wam = 82.5
        student.preferred_location = "Sydney"
        student.availability_start = date.today() + timedelta(days=14)
        student.availability_end = date.today() + timedelta(days=120)
        student.interests = "web, data"
        student.assigned_supervisor = supervisor
        student.save()
        student.skills.set([skills["Python"], skills["Django"], skills["SQL"], skills["Communication"]])

        internship, _ = InternshipListing.objects.get_or_create(
            employer=employer,
            title="Software Engineering Intern",
            defaults={
                "domain": "web",
                "description": "Build Django features, write tests, and support analytics dashboards.",
                "location": "Sydney",
                "duration_weeks": 10,
                "stipend": 1200,
                "work_mode": InternshipListing.WorkMode.HYBRID,
                "start_date": date.today() + timedelta(days=21),
                "application_deadline": date.today() + timedelta(days=10),
                "available_positions": 3,
                "status": InternshipListing.Status.APPROVED,
            },
        )
        internship.required_skills.set([skills["Python"], skills["Django"], skills["SQL"]])

        analytics, _ = InternshipListing.objects.get_or_create(
            employer=employer,
            title="Data Analyst Intern",
            defaults={
                "domain": "data",
                "description": "Prepare reports, clean datasets, and produce placement insights.",
                "location": "Melbourne",
                "duration_weeks": 8,
                "stipend": 900,
                "work_mode": InternshipListing.WorkMode.REMOTE,
                "start_date": date.today() + timedelta(days=28),
                "application_deadline": date.today() + timedelta(days=14),
                "available_positions": 2,
                "status": InternshipListing.Status.APPROVED,
            },
        )
        analytics.required_skills.set([skills["SQL"], skills["Data Analysis"], skills["Python"]])

        application, _ = InternshipApplication.objects.get_or_create(
            student=student,
            internship=internship,
            defaults={
                "cover_letter": "I am interested in applying my Django and SQL skills.",
                "status": InternshipApplication.Status.ACCEPTED,
            },
        )
        WeeklyLog.objects.get_or_create(
            application=application,
            week_start=date.today() - timedelta(days=7),
            defaults={
                "achievements": "Completed onboarding and contributed to dashboard wireframes.",
                "challenges": "Learning the reporting schema.",
                "hours_worked": 35,
            },
        )
        Evaluation.objects.get_or_create(
            application=application,
            supervisor=supervisor,
            defaults={"score": 88, "comments": "Strong technical progress and communication."},
        )
        generate_matches_for_student(student)
        create_notification(student_user, "Welcome to IIPMS", "Your demo student profile is ready.")

        self.stdout.write(self.style.SUCCESS("Demo data created. Password for all demo users: DemoPass123!"))

    def _user(self, username, first_name, last_name, email):
        user, created = User.objects.get_or_create(username=username, defaults={"email": email})
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if created:
            user.set_password(PASSWORD)
        user.save()
        return user

    def _profile(self, user, role, approved):
        profile = user.userprofile
        profile.role = role
        profile.is_approved = approved
        profile.save()
        if role != UserProfile.Role.STUDENT:
            StudentProfile.objects.filter(user=user).delete()
        if role != UserProfile.Role.EMPLOYER:
            EmployerProfile.objects.filter(user=user).delete()
        if role != UserProfile.Role.SUPERVISOR:
            SupervisorProfile.objects.filter(user=user).delete()
        return profile
