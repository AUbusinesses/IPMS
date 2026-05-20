from django.shortcuts import redirect, render

from applications.models import InternshipApplication, WeeklyLog
from supervisors.forms import EvaluationForm
from users.decorators import role_required
from users.models import UserProfile


@role_required(UserProfile.Role.SUPERVISOR)
def supervisor_dashboard(request):
    supervisor = request.user.supervisorprofile
    students = supervisor.students.select_related("user")
    logs = WeeklyLog.objects.filter(
        application__student__assigned_supervisor=supervisor
    ).select_related("application__student__user", "application__internship")
    return render(
        request,
        "supervisors/dashboard.html",
        {"supervisor": supervisor, "students": students, "logs": logs},
    )


@role_required(UserProfile.Role.SUPERVISOR)
def evaluation_create(request):
    supervisor = request.user.supervisorprofile
    form = EvaluationForm(request.POST or None)
    form.fields["application"].queryset = InternshipApplication.objects.filter(
        student__assigned_supervisor=supervisor
    )
    if request.method == "POST" and form.is_valid():
        evaluation = form.save(commit=False)
        evaluation.supervisor = supervisor
        evaluation.save()
        return redirect("supervisor_dashboard")
    return render(request, "supervisors/evaluation_form.html", {"form": form})
