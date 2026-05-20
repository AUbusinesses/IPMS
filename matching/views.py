from django.shortcuts import render

from matching.engine import generate_matches_for_student
from users.decorators import role_required
from users.models import UserProfile


@role_required(UserProfile.Role.STUDENT)
def recommendations(request):
    matches = generate_matches_for_student(request.user.studentprofile)
    return render(request, "students/recommendations.html", {"matches": matches})
