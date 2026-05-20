from django import forms

from applications.models import InternshipApplication, Timesheet, WeeklyLog


class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = ["cover_letter"]


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = ["status", "interview_date", "interview_feedback", "offer_details"]
        widgets = {"interview_date": forms.DateTimeInput(attrs={"type": "datetime-local"})}


class WeeklyLogForm(forms.ModelForm):
    class Meta:
        model = WeeklyLog
        fields = ["application", "week_start", "achievements", "challenges", "hours_worked"]
        widgets = {"week_start": forms.DateInput(attrs={"type": "date"})}


class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ["application", "date", "hours", "task_summary"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
