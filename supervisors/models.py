from django.conf import settings
from django.db import models


class SupervisorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=120, blank=True)
    office_location = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Evaluation(models.Model):
    application = models.ForeignKey(
        "applications.InternshipApplication",
        on_delete=models.CASCADE,
        related_name="evaluations",
    )
    supervisor = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
