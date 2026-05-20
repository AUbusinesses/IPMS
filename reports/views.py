import csv

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from applications.models import InternshipApplication
from employers.models import EmployerProfile
from internships.models import InternshipListing
from students.models import StudentProfile
from users.decorators import role_required
from users.models import UserProfile


def _stats():
    total_students = StudentProfile.objects.count()
    accepted = InternshipApplication.objects.filter(
        status=InternshipApplication.Status.ACCEPTED
    ).count()
    completed = InternshipApplication.objects.filter(evaluations__isnull=False).distinct().count()
    employers = EmployerProfile.objects.count()
    listings = InternshipListing.objects.count()
    applications = InternshipApplication.objects.count()
    return {
        "total_students": total_students,
        "accepted": accepted,
        "placement_rate": round((accepted / total_students) * 100, 1) if total_students else 0,
        "completion_rate": round((completed / accepted) * 100, 1) if accepted else 0,
        "employers": employers,
        "listings": listings,
        "applications": applications,
    }


@role_required(UserProfile.Role.PLACEMENT_OFFICER, UserProfile.Role.ADMIN)
def reports_dashboard(request):
    stats = _stats()
    status_counts = InternshipApplication.objects.values("status").annotate(total=Count("id"))
    students = StudentProfile.objects.select_related("user", "assigned_supervisor")
    employers = EmployerProfile.objects.select_related("user")
    pending_employers = employers.filter(is_verified=False)
    pending_internships = InternshipListing.objects.filter(status=InternshipListing.Status.PENDING)
    return render(
        request,
        "reports/dashboard.html",
        {
            "stats": stats,
            "status_counts": list(status_counts),
            "students": students,
            "employers": employers,
            "pending_employers": pending_employers,
            "pending_internships": pending_internships,
        },
    )


@role_required(UserProfile.Role.PLACEMENT_OFFICER, UserProfile.Role.ADMIN)
def approve_employer(request, pk):
    employer = get_object_or_404(EmployerProfile, pk=pk)
    employer.is_verified = True
    employer.save(update_fields=["is_verified"])
    employer.user.userprofile.is_approved = True
    employer.user.userprofile.save(update_fields=["is_approved"])
    return redirect("reports_dashboard")


@role_required(UserProfile.Role.PLACEMENT_OFFICER, UserProfile.Role.ADMIN)
def approve_internship(request, pk):
    internship = get_object_or_404(InternshipListing, pk=pk)
    internship.status = InternshipListing.Status.APPROVED
    internship.save(update_fields=["status"])
    return redirect("reports_dashboard")


@role_required(UserProfile.Role.PLACEMENT_OFFICER, UserProfile.Role.ADMIN)
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="iipms_report.csv"'
    writer = csv.writer(response)
    writer.writerow(["Metric", "Value"])
    for key, value in _stats().items():
        writer.writerow([key.replace("_", " ").title(), value])
    writer.writerow([])
    writer.writerow(["Application", "Student", "Internship", "Employer", "Status"])
    for application in InternshipApplication.objects.select_related(
        "student__user", "internship__employer"
    ):
        writer.writerow(
            [
                application.id,
                application.student.user.get_full_name(),
                application.internship.title,
                application.internship.employer.company_name,
                application.get_status_display(),
            ]
        )
    return response


@role_required(UserProfile.Role.PLACEMENT_OFFICER, UserProfile.Role.ADMIN)
def export_pdf(request):
    lines = ["IIPMS Analytics Report"]
    lines.extend(f"{key.replace('_', ' ').title()}: {value}" for key, value in _stats().items())
    content = "BT /F1 16 Tf 18 TL 72 740 Td "
    content += " T* ".join(f"({line}) Tj" for line in lines)
    content += " ET"
    pdf = _minimal_pdf(content)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="iipms_report.pdf"'
    return response


def _minimal_pdf(stream):
    stream_bytes = stream.encode("latin-1", errors="replace")
    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n",
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
        b"5 0 obj << /Length "
        + str(len(stream_bytes)).encode()
        + b" >> stream\n"
        + stream_bytes
        + b"\nendstream endobj\n",
    ]
    pdf = b"%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf += obj
    xref = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets[1:]:
        pdf += f"{offset:010d} 00000 n \n".encode()
    pdf += (
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF"
    ).encode()
    return pdf
