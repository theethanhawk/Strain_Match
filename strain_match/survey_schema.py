# strain_match/survey_schema.py

# All questions required in this pass (you can toggle per item later)
REQ = True

# Choice banks (single-use or reuse)
EFFECTS_DESIRED = [
    ("calm_relax", "Calm/Relaxation"),
    ("sleep", "Sleep Support"),
    ("focus", "Focus/Clarity"),
    ("euphoria", "Euphoria"),
    ("creativity", "Creativity"),
    ("pain_relief", "Pain Relief"),
    ("energy", "Energy/Uplift"),
]

CONSUMPTION_FREQ = [
    ("rarely", "Rarely (once a month or less)"),
    ("occasionally", "Occasionally (2–3 times a month)"),
    ("frequently", "Frequently (1–2 times weekly)"),
    ("often", "Often (3–5 times a week)"),
    ("daily", "Daily"),
]

TIMES_OF_DAY = [
    ("morning", "Morning"),
    ("afternoon", "Afternoon"),
    ("evening", "Evening"),
    ("late_night", "Late Night"),
]

METHODS_PREFERRED_ONE = [
    ("flower", "Flower"),
    ("vape", "Vape"),
    ("edible", "Edible"),
    ("extract", "Extract"),
]

METHODS_MULTI = [
    ("joint", "Joint"),
    ("bong", "Bong"),
    ("pipe", "Pipe"),
    ("vape", "Vape"),
    ("blunt", "Blunt"),
    ("edible", "Edible"),
    ("other", "Other"),
]

EFFECTS_AVOID = [
    ("anxiety", "Anxiety/Paranoia"),
    ("groggy", "Grogginess"),
    ("racing_thoughts", "Racing Thoughts"),
]

STRAIN_TYPE = [
    ("sativa", "Sativa"),
    ("indica", "Indica"),
    ("hybrid", "Hybrid"),
]

YES_NO = [("yes", "Yes"), ("no", "No")]

PRIMARY_FLAVOR = [
    ("citrus", "Citrus"),
    ("fruity", "Fruity"),
    ("earthy", "Earthy"),
    ("piney_fuel", "Piney/Fuel"),
    ("floral", "Floral"),
]

TIME_TO_ONSET = [
    ("lt30", "Less than 30 min"),
    ("30_60", "30–60 min"),
    ("gt60", "More than an hour"),
    ("gt120", "More than two hours"),
]

PHYSICAL_INTENSITY = [
    ("head", "Head"),
    ("face", "Face"),
    ("limbs", "Limbs"),
    ("body", "Body"),
    ("stomach", "Stomach"),
    ("analgesic", "Analgesic"),
]

MENTAL_INTENSITY = [
    ("euphoric", "Euphoric"),
    ("relaxed", "Relaxed"),
    ("energized", "Energized"),
    ("tired", "Tired"),
    ("anxious", "Anxious"),
    ("creative", "Creative"),
]

DURATION = [
    ("1h", "1 hour"),
    ("2h", "2 hours"),
    ("3h", "3 hours"),
    ("4h", "4 hours"),
    ("5h", "5 hours"),
    ("gt5h", "More than 5 hours"),
]

LOCATION = [
    ("home", "Home"),
    ("work", "Work"),
    ("indoor", "Indoor"),
    ("outdoor", "Outdoor"),
    ("other", "Other"),
]

ACTIVITY = [
    ("social", "Social"),
    ("artistic", "Artistic"),
    ("physical", "Physical"),
    ("work", "Work"),
    ("study", "Study"),
]

# Wizard order: grouped for a natural flow
SURVEY_SCHEMA = [
    # Preferences
    {"slug": "desired_effects", "label": "Desired effects", "type": "multi",
     "choices": EFFECTS_DESIRED, "required": REQ,
     "help": "Select one to three that best match your goals."},

    {"slug": "preferred_strain_type", "label": "Preferred strain type", "type": "choice",
     "choices": STRAIN_TYPE, "required": REQ},

    {"slug": "primary_flavor_aroma", "label": "Primary flavor/aroma", "type": "choice",
     "choices": PRIMARY_FLAVOR, "required": REQ},

    # Usage
    {"slug": "consumption_frequency", "label": "Consumption frequency", "type": "choice",
     "choices": CONSUMPTION_FREQ, "required": REQ},

    {"slug": "preferred_time_of_day", "label": "Preferred time of day", "type": "multi",
     "choices": TIMES_OF_DAY, "required": REQ},

    {"slug": "consumption_method", "label": "Consumption method", "type": "multi",
     "choices": METHODS_MULTI, "required": REQ},

    {"slug": "preferred_consumption_method", "label": "Preferred consumption method", "type": "choice",
     "choices": METHODS_PREFERRED_ONE, "required": REQ},

    # Effects (avoid & intensities)
    {"slug": "effects_to_avoid", "label": "Effects to avoid", "type": "multi",
     "choices": EFFECTS_AVOID, "required": REQ},

    {"slug": "physical_intensity", "label": "Physical intensity areas", "type": "multi",
     "choices": PHYSICAL_INTENSITY, "required": REQ},

    {"slug": "mental_intensity", "label": "Mental intensity qualities", "type": "multi",
     "choices": MENTAL_INTENSITY, "required": REQ},

    # Experience curve
    {"slug": "time_to_onset", "label": "Time to onset", "type": "choice",
     "choices": TIME_TO_ONSET, "required": REQ},

    {"slug": "duration", "label": "Duration", "type": "choice",
     "choices": DURATION, "required": REQ},

    # Wellness flags (kept as choice to match your “Boolean Yes/No”, UI will still use “single pick”)
    {"slug": "sleep_issues", "label": "Do you have sleep issues?", "type": "choice",
     "choices": YES_NO, "required": REQ},

    {"slug": "anxiety_prone", "label": "Are you prone to anxiety?", "type": "choice",
     "choices": YES_NO, "required": REQ},

    # Context
    {"slug": "location", "label": "Location", "type": "multi",
     "choices": LOCATION, "required": REQ},

    {"slug": "activity", "label": "Activity", "type": "multi",
     "choices": ACTIVITY, "required": REQ},

    # Satisfaction (1–10). You requested “all checkboxes” in UI, so we’ll render 1..10 as 10 checkboxes and enforce single selection in JS.
    {"slug": "overall_satisfaction", "label": "Overall satisfaction (1–10)", "type": "int",
     "min": 1, "max": 10, "required": REQ,
     "help": "Pick the number that best matches your typical experience."},
]
