"""
Django admin configuration for the analyzer app.
Allows managing ResumeAnalysis records from Django admin panel.
"""

from django.contrib import admin
from .models import ResumeAnalysis


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    """
    Admin interface for ResumeAnalysis model.
    """
    list_display = ['id', 'match_score', 'created_at']
    list_filter = ['created_at', 'match_score']
    search_fields = ['job_description', 'resume_text']
    readonly_fields = ['resume_text', 'created_at', 'updated_at']
    fieldsets = (
        ('File Information', {
            'fields': ['resume_file']
        }),
        ('Extracted Content', {
            'fields': ['resume_text']
        }),
        ('Job Description', {
            'fields': ['job_description']
        }),
        ('Analysis Results', {
            'fields': ['match_score', 'matched_skills', 'missing_skills']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at']
        }),
    )