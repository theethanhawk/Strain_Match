from django.urls import path
from . import views

app_name = "strain_match"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('welcome/', views.welcome, name='welcome'),
    path('survey/', views.survey, name='survey'),
    path('about/', views.about, name='about'),
    path('faqs/', views.faqs, name='faqs'),
    path('myprofile/', views.myprofile, name='myprofile'),
    #path("age-verify/", views.age_verify, name="age_verify"),
]