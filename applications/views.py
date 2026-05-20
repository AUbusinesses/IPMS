from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from applications.forms import (
    ApplicationStatusForm,
    InternshipApplicationForm,
    TimesheetForm,
    WeeklyLogForm,
)
from applications.models import InternshipApplication
from internships.models import InternshipListing
from notifications.utils import create_notification
from users.decorators import role_required
from users.models import UserProfile


@role_required(UserProfile.Role.STUDENT)
def apply_to_internship(request, internship_id):
    internship = get_object_or_404(
        InternshipListing, pk=internship_id, status=InternshipListing.Status.APPROVED
    )
    form = InternshipApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application, created = InternshipApplication.objects.get_or_create(
            student=request.user.studentprofile,
            internship=internship,
            defaults={"cover_letter": form.cleaned_data["cover_letter"]},
        )
        if created:
            create_notification(
                internship.employer.user,
                "New internship application",
                f"{request.user.get_full_name()} applied for {internship.title}.",
            )
            messages.success(request, "Application submitted.")
        else:
            messages.info(request, "You have already applied for this internship.")
        return redirect("student_dashboard")
    return render(request, "applications/apply.html", {"form": form, "internship": internship})


@login_required
def applications_list(request):
    role = request.user.userprofile.role
    if role == UserProfile.Role.STUDENT:
        applications = InternshipApplication.objects.filter(
            student=request.user.studentprofile
        )
    elif role == UserProfile.Role.EMPLOYER:
        applications = InternshipApplication.objects.filter(
            internship__employer=request.user.employerprofile
        )
    else:
        applications = InternshipApplication.objects.all()
    return render(request, "applications/list.html", {"applications": applications})


@role_required(UserProfile.Role.EMPLOYER, UserProfile.Role.PLACEMENT_OFFICER, UserProfile.Role.ADMIN)
def update_application(request, pk):
    application = get_object_or_404(InternshipApplication, pk=pk)
    form = ApplicationStatusForm(request.POST or None, instance=application)
    if request.method == "POST" and form.is_valid():
        form.save()
        create_notification(
            application.student.user,
            "Application updated",
            f"Your application for {application.internship.title} is now {application.get_status_display()}.",
        )
        messages.success(request, "Application updated.")
        return redirect("applications_list")
    return render(request, "applications/status_form.html", {"form": form, "application": application})


@role_required(UserProfile.Role.STUDENT)
def weekly_log_create(request):
    form = WeeklyLogForm(request.POST or None)
    form.fields["application"].queryset = InternshipApplication.objects.filter(
        student=request.user.studentprofile,
        status__in=[
            InternshipApplication.Status.ACCEPTED,
            InternshipApplication.Status.OFFERED,
        ],
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Weekly log submitted.")
        return redirect("student_dashboard")
    return render(request, "applications/weekly_log_form.html", {"form": form})


@role_required(UserProfile.Role.STUDENT)
def timesheet_create(request):
    form = TimesheetForm(request.POST or None)
    form.fields["application"].queryset = InternshipApplication.objects.filter(
        student=request.user.studentprofile,
        status=InternshipApplication.Status.ACCEPTED,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Timesheet submitted.")
        return redirect("student_dashboard")
    return render(request, "applications/timesheet_form.html", {"form": form})
