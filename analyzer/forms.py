"""
Forms for the Resume Analyzer application.

Forms:
- ResumeAnalysisForm: Form for uploading resume and entering job description
  Fields:
    - resume_file: PDF file upload
    - job_description: Text area for job description
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import ResumeAnalysis
import os


class ResumeAnalysisForm(forms.ModelForm):
    """
    Form for resume upload and job description input.
    Validates file type and content.
    """
    
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 8,
            'placeholder': '''Paste the complete job description here. Include:
- Job title and responsibilities
- Required skills and qualifications
- Experience requirements
- Any specific tools or technologies needed

Example:
Senior Python Developer
5+ years experience
Skills: Django, REST APIs, Machine Learning, PostgreSQL
Responsibilities: Build scalable backend systems, optimize performance...''',
            'class': 'form-control',
        }),
        label='Job Description',
        help_text='The more detailed the job description, the more accurate the analysis.'
    )
    
    class Meta:
        model = ResumeAnalysis
        fields = ['resume_file', 'job_description']
        widgets = {
            'resume_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True,
            }),
        }
        labels = {
            'resume_file': 'Upload Your Resume (PDF only)',
        }
    
    def clean_resume_file(self):
        """
        Validate resume file:
        - Must be a PDF file
        - File size must be less than 10MB
        """
        resume_file = self.cleaned_data.get('resume_file')
        
        if resume_file:
            # Check file extension
            file_name = resume_file.name
            file_ext = os.path.splitext(file_name)[1].lower()
            
            if file_ext != '.pdf':
                raise ValidationError('Only PDF files are allowed. Please upload a PDF resume.')
            
            # Check file size (10MB limit)
            if resume_file.size > 10 * 1024 * 1024:  # 10MB
                raise ValidationError('File size must not exceed 10MB. Please upload a smaller file.')
        
        return resume_file
    
    def clean_job_description(self):
        """
        Validate job description:
        - Must not be empty
        - Minimum length of 50 characters
        """
        job_description = self.cleaned_data.get('job_description')
        
        if not job_description:
            raise ValidationError('Job description is required.')
        
        if len(job_description.strip()) < 50:
            raise ValidationError('Job description must be at least 50 characters long.')
        
        return job_description
