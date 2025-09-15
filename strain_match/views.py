# strain_match/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SurveyForm
from .models import Survey
from .survey_schema import SURVEY_SCHEMA


def user_has_survey(user) -> bool:
    """DB-safe check for the one-time survey."""
    return Survey.objects.filter(user=user).exists()


@login_required
def home(request):
    """Main in-app landing; gated behind the initial survey."""
    if not user_has_survey(request.user):
        return redirect("strain_match:welcome")
    return render(request, "strain_match/home.html")


@login_required
def welcome(request):
    """Welcome page prompting users to take the one-time survey."""
    if user_has_survey(request.user):
        messages.info(request, "Welcome back!")
        return redirect("strain_match:home")
    return render(request, "strain_match/welcome.html")


@login_required
def survey(request):
    """
    One-time survey (schema-driven). The UI (survey.html) renders a JS wizard that
    posts hidden q__<slug> fields. Server still validates & saves via SurveyForm.
    """
    if user_has_survey(request.user):
        messages.info(request, "You’ve already completed your initial survey.")
        return redirect("strain_match:home")

    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.user = request.user

            # TEMP defaults for legacy typed columns so we can keep UI JSON-only.
            # (We can later map JSON keys -> typed fields or remove these columns.)
            if not getattr(survey, "goal", None):
                survey.goal = "relaxation"       # must be a valid choice from your Goal enum
            if not getattr(survey, "experience_level", None):
                survey.experience_level = "casual"
            if getattr(survey, "tolerance", None) in (None, ""):
                survey.tolerance = 5
            if not getattr(survey, "preferred_time", None):
                survey.preferred_time = "anytime"

            if survey.extra is None:
                survey.extra = {}

            survey.save()
            messages.success(request, "Survey saved! Welcome to Strain Match.")
            return redirect("strain_match:home")
    else:
        form = SurveyForm()

    # Pass schema for the wizard UI (the template will JSON-encode it safely)
    return render(request, "strain_match/survey.html", {"form": form, "schema": SURVEY_SCHEMA})


def about(request):
    """Static About page."""
    return render(request, "strain_match/about.html")


def faqs(request):
    """Static FAQs page."""
    return render(request, "strain_match/faqs.html")


@login_required
def myprofile(request):
    """Basic profile view; shows survey status/details if present."""
    return render(request, "strain_match/myprofile.html")
