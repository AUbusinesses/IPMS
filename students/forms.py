from django import forms

from students.models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            "student_id",
            "course",
            "gpa_wam",
            "preferred_location",
            "availability_start",
            "availability_end",
            "interests",
            "resume",
            "skills",
        ]
        widgets = {
            "availability_start": forms.DateInput(attrs={"type": "date"}),
            "availability_end": forms.DateInput(attrs={"type": "date"}),
            "skills": forms.CheckboxSelectMultiple,
        }
