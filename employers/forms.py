from django import forms

from employers.models import EmployerProfile


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ["company_name", "industry", "website", "location", "description"]
