"""
Database Models for the Resume Analyzer application.

Models:
- ResumeAnalysis: Stores each resume analysis result
  Fields:
    - id: Auto-generated primary key
    - resume_file: Uploaded PDF file path
    - resume_text: Extracted text from resume
    - job_description: Job description provided by user
    - match_score: Calculated match percentage (0-100)
    - matched_skills: Skills found in both resume and job description
    - missing_skills: Skills in job description but not in resume
    - created_at: Timestamp of analysis
    - updated_at: Last update timestamp
"""
from django.conf import settings
from django.db import models
import os


class ResumeAnalysis(models.Model):
    """
    Model to store resume analysis results.
    Each record represents one analysis session.
    """
    
    # Store the uploaded PDF file
    resume_file = models.FileField(
        upload_to='resumes/',
        help_text='Uploaded resume PDF file'
    )
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name='resume_analyses'
)
    
    # Store extracted text from resume
    resume_text = models.TextField(
        help_text='Text extracted from resume PDF'
    )
    
    # Store job description provided by user
    job_description = models.TextField(
        help_text='Job description provided by user'
    )
    
    # Match score calculated by ML model
    match_score = models.FloatField(
        default=0.0,
        help_text='Match percentage between resume and job description (0-100)'
    )
    
    # Skills found in both resume and job description
    matched_skills = models.TextField(
        blank=True,
        help_text='Comma-separated list of matched skills'
    )
    
    # Skills in job description but not in resume
    missing_skills = models.TextField(
        blank=True,
        help_text='Comma-separated list of missing skills'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the analysis was created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the analysis was last updated'
    )
    
    class Meta:
        """Model metadata"""
        ordering = ['-created_at']  # Show newest first
        verbose_name = 'Resume Analysis'
        verbose_name_plural = 'Resume Analyses'
    
    def __str__(self):
        """String representation of the model"""
        return f"Analysis - {self.match_score}% Match - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_matched_skills_list(self):
        """Return matched skills as a list"""
        if self.matched_skills:
            return [skill.strip() for skill in self.matched_skills.split(',')]
        return []
    
    def get_missing_skills_list(self):
        """Return missing skills as a list"""
        if self.missing_skills:
            return [skill.strip() for skill in self.missing_skills.split(',')]
        return []
