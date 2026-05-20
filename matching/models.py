from django.db import models


class MatchRecord(models.Model):
    student = models.ForeignKey(
        "students.StudentProfile", on_delete=models.CASCADE, related_name="matches"
    )
    internship = models.ForeignKey(
        "internships.InternshipListing", on_delete=models.CASCADE, related_name="matches"
    )
    score = models.PositiveSmallIntegerField(db_index=True)
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "internship")
        ordering = ["-score"]

    def __str__(self):
        return f"{self.student} - {self.internship}: {self.score}%"
