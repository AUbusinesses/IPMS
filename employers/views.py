from django.shortcuts import redirect, render

from applications.models import InternshipApplication
from employers.forms import EmployerProfileForm
from users.decorators import role_required
from users.models import UserProfile


@role_required(UserProfile.Role.EMPLOYER)
def employer_dashboard(request):
    employer = request.user.employerprofile
    internships = employer.internships.all()
    applications = InternshipApplication.objects.filter(
        internship__employer=employer
    ).select_related("student__user", "internship")
    return render(
        request,
        "employers/dashboard.html",
        {"employer": employer, "internships": internships, "applications": applications},
    )


@role_required(UserProfile.Role.EMPLOYER)
def employer_profile(request):
    employer = request.user.employerprofile
    form = EmployerProfileForm(request.POST or None, instance=employer)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("employer_dashboard")
    return render(request, "employers/profile.html", {"form": form})
