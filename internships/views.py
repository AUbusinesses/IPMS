from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from applications.forms import InternshipApplicationForm
from internships.forms import InternshipListingForm
from internships.models import InternshipListing
from users.decorators import role_required
from users.models import UserProfile


@login_required
def internship_list(request):
    query = request.GET.get("q", "")
    location = request.GET.get("location", "")
    internships = InternshipListing.objects.filter(status=InternshipListing.Status.APPROVED)
    if query:
        internships = internships.filter(
            Q(title__icontains=query)
            | Q(domain__icontains=query)
            | Q(required_skills__name__icontains=query)
        ).distinct()
    if location:
        internships = internships.filter(location__icontains=location)
    return render(
        request,
        "internships/list.html",
        {"internships": internships, "query": query, "location": location},
    )


@login_required
def internship_detail(request, pk):
    internship = get_object_or_404(InternshipListing, pk=pk)
    application_form = InternshipApplicationForm()
    return render(
        request,
        "internships/detail.html",
        {"internship": internship, "application_form": application_form},
    )


@role_required(UserProfile.Role.EMPLOYER)
def internship_create(request):
    employer = request.user.employerprofile
    form = InternshipListingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        internship = form.save(commit=False)
        internship.employer = employer
        internship.status = InternshipListing.Status.PENDING
        internship.save()
        form.save_m2m()
        messages.success(request, "Internship submitted for approval.")
        return redirect("employer_dashboard")
    return render(request, "internships/form.html", {"form": form})


@role_required(UserProfile.Role.EMPLOYER)
def internship_edit(request, pk):
    internship = get_object_or_404(
        InternshipListing, pk=pk, employer=request.user.employerprofile
    )
    form = InternshipListingForm(request.POST or None, instance=internship)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Internship updated.")
        return redirect("employer_dashboard")
    return render(request, "internships/form.html", {"form": form, "internship": internship})
