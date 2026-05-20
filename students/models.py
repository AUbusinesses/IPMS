from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_resume(file):
    allowed = [".pdf", ".doc", ".docx"]
    if not any(file.name.lower().endswith(ext) for ext in allowed):
        raise ValidationError("Resume must be a PDF, DOC, or DOCX file.")
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("Resume must be 5MB or smaller.")


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=40, blank=True, db_index=True)
    course = models.CharField(max_length=120, blank=True)
    gpa_wam = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    preferred_location = models.CharField(max_length=120, blank=True)
    availability_start = models.DateField(null=True, blank=True)
    availability_end = models.DateField(null=True, blank=True)
    interests = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated domains such as data, web, cyber security.",
    )
    resume = models.FileField(
        upload_to="resumes/",
        validators=[validate_resume],
        blank=True,
        null=True,
    )
    skills = models.ManyToManyField("internships.Skill", blank=True, related_name="students")
    assigned_supervisor = models.ForeignKey(
        "supervisors.SupervisorProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
