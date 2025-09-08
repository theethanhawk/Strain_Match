# strain_match/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SurveyForm
from .models import Survey

def user_has_survey(user) -> bool:
    # Query the DB to avoid RelatedObjectDoesNotExist on reverse OneToOne access
    return Survey.objects.filter(user=user).exists()

@login_required
def home(request):
    if not user_has_survey(request.user):
        return redirect("strain_match:welcome")
    return render(request, "strain_match/home.html")

@login_required
def welcome(request):
    if user_has_survey(request.user):
        messages.info(request, "Welcome back!")
        return redirect("strain_match:home")
    return render(request, "strain_match/welcome.html")

@login_required
def survey(request):
    # One-time survey: if already present, send home
    if user_has_survey(request.user):
        messages.info(request, "You’ve already completed your initial survey.")
        return redirect("strain_match:home")

    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.user = request.user
            if survey.extra is None:  # just in case
                survey.extra = {}
            survey.save()
            messages.success(request, "Survey saved! Welcome to Strain Match.")
            return redirect("strain_match:home")
    else:
        form = SurveyForm()

    return render(request, "strain_match/survey.html", {"form": form})

def about(request):
    return render(request, "strain_match/about.html")

def faqs(request):
    return render(request, "strain_match/faqs.html")

@login_required
def myprofile(request):
    return render(request, "strain_match/myprofile.html")
