from django.shortcuts import redirect, render

from applications.models import InternshipApplication
from matching.engine import generate_matches_for_student
from students.forms import StudentProfileForm
from users.decorators import role_required
from users.models import UserProfile


@role_required(UserProfile.Role.STUDENT)
def student_dashboard(request):
    student = request.user.studentprofile
    applications = InternshipApplication.objects.filter(student=student).select_related(
        "internship"
    )
    recommendations = generate_matches_for_student(student)[:5]
    return render(
        request,
        "students/dashboard.html",
        {
            "student": student,
            "applications": applications,
            "recommendations": recommendations,
        },
    )


@role_required(UserProfile.Role.STUDENT)
def student_profile(request):
    student = request.user.studentprofile
    form = StudentProfileForm(request.POST or None, request.FILES or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("student_dashboard")
    return render(request, "students/profile.html", {"form": form})
