from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("after-login/", views.post_login, name="post_login"),
]
