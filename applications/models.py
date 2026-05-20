from django.db import models


class InternshipApplication(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        SHORTLISTED = "shortlisted", "Shortlisted"
        INTERVIEW = "interview", "Interview"
        OFFERED = "offered", "Offered"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    student = models.ForeignKey(
        "students.StudentProfile", on_delete=models.CASCADE, related_name="applications"
    )
    internship = models.ForeignKey(
        "internships.InternshipListing",
        on_delete=models.CASCADE,
        related_name="applications",
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SUBMITTED, db_index=True
    )
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_feedback = models.TextField(blank=True)
    offer_details = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "internship")
        ordering = ["-applied_at"]
        indexes = [models.Index(fields=["status", "applied_at"])]

    def __str__(self):
        return f"{self.student} -> {self.internship}"


class WeeklyLog(models.Model):
    application = models.ForeignKey(
        InternshipApplication, on_delete=models.CASCADE, related_name="weekly_logs"
    )
    week_start = models.DateField()
    achievements = models.TextField()
    challenges = models.TextField(blank=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    supervisor_comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("application", "week_start")
        ordering = ["-week_start"]


class Timesheet(models.Model):
    application = models.ForeignKey(
        InternshipApplication, on_delete=models.CASCADE, related_name="timesheets"
    )
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    task_summary = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("application", "date")
        ordering = ["-date"]
