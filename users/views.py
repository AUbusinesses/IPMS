from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from users.forms import RegisterForm
from users.models import UserProfile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration complete.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def dashboard(request):
    profile = request.user.userprofile
    if not profile.is_approved and profile.role not in [
        UserProfile.Role.STUDENT,
        UserProfile.Role.ADMIN,
    ]:
        return render(request, "users/pending.html")
    if profile.role == UserProfile.Role.STUDENT:
        return redirect("student_dashboard")
    if profile.role == UserProfile.Role.EMPLOYER:
        return redirect("employer_dashboard")
    if profile.role == UserProfile.Role.SUPERVISOR:
        return redirect("supervisor_dashboard")
    if profile.role in [UserProfile.Role.PLACEMENT_OFFICER, UserProfile.Role.ADMIN]:
        return redirect("reports_dashboard")
    return render(request, "users/pending.html")
