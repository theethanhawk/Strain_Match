# strain_match/admin.py
from django.contrib import admin
from .models import Survey

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("user", "goal", "experience_level", "tolerance", "preferred_time", "updated_at")
    list_filter = ("goal", "experience_level", "preferred_time")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
