from django.conf import settings
from django.db import models
from django.utils import timezone


class Skill(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class InternshipListing(models.Model):
    class WorkMode(models.TextChoices):
        ONSITE = "onsite", "On-site"
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending Approval"
        APPROVED = "approved", "Approved"
        CLOSED = "closed", "Closed"
        REJECTED = "rejected", "Rejected"

    employer = models.ForeignKey(
        "employers.EmployerProfile",
        on_delete=models.CASCADE,
        related_name="internships",
    )
    title = models.CharField(max_length=160, db_index=True)
    domain = models.CharField(max_length=120, db_index=True)
    description = models.TextField()
    required_skills = models.ManyToManyField(Skill, related_name="internships")
    location = models.CharField(max_length=120, db_index=True)
    duration_weeks = models.PositiveIntegerField()
    stipend = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    work_mode = models.CharField(max_length=20, choices=WorkMode.choices)
    start_date = models.DateField()
    application_deadline = models.DateField(db_index=True)
    available_positions = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "application_deadline"])]

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return self.application_deadline < timezone.localdate()
