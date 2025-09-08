from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CustomUserCreationForm, CustomAuthenticationForm


def landing(request):
    """
    Public landing page with quick links to Sign Up / Log In.
    If already authenticated, send them onward.
    """
    if request.user.is_authenticated:
        # TODO: After the strain_match app exists, change this to its home route.
        return redirect("users:post_login")
    return render(request, "users/landing.html")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("users:post_login")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            # TODO: change to 'strain_match:home' once built
            return redirect("users:post_login")
    else:
        form = CustomUserCreationForm()

    return render(request, "users/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("users:post_login")

    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Try auth by username OR email
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                # Try treating the field as email
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    u = User.objects.get(email__iexact=username_or_email.strip())
                    user = authenticate(request, username=u.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                # TODO: change to 'strain_match:home' once built
                return redirect("users:post_login")
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = CustomAuthenticationForm(request)

    return render(request, "users/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect("users:landing")
    # For safety, redirect if someone GETs this URL
    return redirect("users:landing")


@login_required
def post_login(request):
    """
    Temporary 'you are in' page until the Strain Match app Home exists.
    Replace redirects to this view with 'strain_match:home' later.
    """
    return render(request, "users/post_login.html")
