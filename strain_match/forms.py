# strain_match/forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Survey
from .survey_schema import SURVEY_SCHEMA


class SurveyForm(forms.ModelForm):
    """
    Dynamic schema-driven survey.
    - Builds fields named q__<slug> from SURVEY_SCHEMA
    - Bundles cleaned values into instance.extra
    - Does NOT require legacy typed fields (we set safe defaults in the view)
    """

    class Meta:
        model = Survey
        fields = []  # <- no legacy typed fields; we submit only dynamic q__* answers

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for q in SURVEY_SCHEMA:
            slug = q["slug"]
            field_name = f"q__{slug}"
            ftype = q["type"]
            label = q.get("label", slug.replace("_", " ").title())
            help_text = q.get("help", "")
            required = q.get("required", True)

            field = self._build_field(ftype, q, label, required, help_text)
            self.fields[field_name] = field

        self.order_fields([f"q__{q['slug']}" for q in SURVEY_SCHEMA])

    def _build_field(self, ftype, q, label, required, help_text):
        if ftype == "choice":
            return forms.ChoiceField(
                label=label,
                choices=self._normalize_choices(q.get("choices", [])),
                required=required,
                help_text=help_text,
            )
        if ftype == "multi":
            return forms.MultipleChoiceField(
                label=label,
                choices=self._normalize_choices(q.get("choices", [])),
                required=required,
                help_text=help_text,
            )
        if ftype == "int":
            return forms.IntegerField(
                label=label,
                required=required,
                help_text=help_text,
                min_value=q.get("min"),
                max_value=q.get("max"),
            )
        if ftype == "float":
            return forms.FloatField(
                label=label,
                required=required,
                help_text=help_text,
                min_value=q.get("min"),
                max_value=q.get("max"),
            )
        if ftype == "bool":
            return forms.BooleanField(label=label, required=required, help_text=help_text)
        if ftype == "text":
            return forms.CharField(label=label, required=required, help_text=help_text)
        if ftype == "tags":
            return forms.CharField(label=label, required=required, help_text=help_text)
        raise ValidationError(f"Unsupported field type: {ftype}")

    def _normalize_choices(self, raw):
        norm = []
        for item in raw:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                norm.append((item[0], item[1]))
            else:
                norm.append((item, str(item).title()))
        return norm

    def clean(self):
        cleaned = super().clean()

        # Enforce "Desired effects: select one to three" if present
        name = "q__desired_effects"
        if name in self.fields:
            vals = self.cleaned_data.get(name) or []
            if not (1 <= len(vals) <= 3):
                self.add_error(name, "Please select between 1 and 3 effects.")

        # Bundle all answers into JSON
        bundle = {}
        for q in SURVEY_SCHEMA:
            slug = q["slug"]
            fname = f"q__{slug}"
            ftype = q["type"]
            val = self.cleaned_data.get(fname)

            if ftype == "tags":
                if val is None or val == "":
                    val = []
                elif isinstance(val, str):
                    val = [t.strip() for t in val.split(",") if t.strip()]

            bundle[slug] = val

        self._extra_bundle = bundle
        return cleaned

    def save(self, commit=True):
        instance: Survey = super().save(commit=False)
        instance.extra = getattr(self, "_extra_bundle", {}) or {}
        if commit:
            instance.save()
        return instance
