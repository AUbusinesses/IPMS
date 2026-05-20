from django import forms

from supervisors.models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["application", "score", "comments"]

    def clean_score(self):
        score = self.cleaned_data["score"]
        if score > 100:
            raise forms.ValidationError("Score must be between 0 and 100.")
        return score
