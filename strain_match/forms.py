# strain_match/forms.py
from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    extra = forms.JSONField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": '{"avoid_anxiety": true, "terpenes": ["limonene","linalool"]}',
            }
        ),
        help_text="Optional JSON for additional preferences. Leave blank if not needed.",
    )

    class Meta:
        model = Survey
        fields = ["goal", "experience_level", "tolerance", "preferred_time", "notes", "extra"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Any notes or sensitivities…"})}

    def clean_tolerance(self):
        tol = self.cleaned_data.get("tolerance")
        if tol is None:
            return tol
        if not (0 <= tol <= 10):
            raise forms.ValidationError("Tolerance must be between 0 and 10.")
        return tol

    def clean_extra(self):
        extra = self.cleaned_data.get("extra")
        # If left blank, JSONField returns None — coerce to {}
        return extra if isinstance(extra, (dict, list)) else {}
