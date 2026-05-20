from django import forms

from internships.models import InternshipListing, Skill


class InternshipListingForm(forms.ModelForm):
    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = InternshipListing
        fields = [
            "title",
            "domain",
            "description",
            "required_skills",
            "location",
            "duration_weeks",
            "stipend",
            "work_mode",
            "start_date",
            "application_deadline",
            "available_positions",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "application_deadline": forms.DateInput(attrs={"type": "date"}),
        }
