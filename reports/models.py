from django.db import models


class GeneratedReport(models.Model):
    title = models.CharField(max_length=160)
    report_type = models.CharField(max_length=80)
    generated_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title
