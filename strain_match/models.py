# strain_match/models.py
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Goal(models.TextChoices):
    SLEEP = "sleep", "Sleep"
    PAIN = "pain", "Pain"
    FOCUS = "focus", "Focus"
    CREATIVITY = "creativity", "Creativity"
    RELAXATION = "relaxation", "Relaxation"
    ENERGY = "energy", "Energy"


class ExperienceLevel(models.TextChoices):
    NEW = "new", "New"
    CASUAL = "casual", "Casual"
    REGULAR = "regular", "Regular"
    HEAVY = "heavy", "Heavy"


class PreferredTime(models.TextChoices):
    MORNING = "morning", "Morning"
    AFTERNOON = "afternoon", "Afternoon"
    EVENING = "evening", "Evening"
    ANYTIME = "anytime", "Anytime"


class Survey(models.Model):
    """
    One-time initial survey per user (MVP).
    Keep core fields typed; 'extra' JSON allows flexible additions without migrations.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="survey",
    )

    # Core typed fields
    goal = models.CharField(max_length=16, choices=Goal.choices)
    experience_level = models.CharField(max_length=16, choices=ExperienceLevel.choices)
    tolerance = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="0 = very low, 10 = very high",
    )
    preferred_time = models.CharField(max_length=16, choices=PreferredTime.choices)
    notes = models.TextField(blank=True)

    # Flexible extras (no migrations needed when you add keys)
    extra = models.JSONField(default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        return f"Survey for {self.user.username}"
