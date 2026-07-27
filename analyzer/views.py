"""
Views for the Resume Analyzer application.

Views:
- index: Home page
- analyze: Handle resume upload and analysis
- results: Display analysis results
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ResumeAnalysisForm
from .models import ResumeAnalysis
from .ml_utils import ResumeAnalyzer
import os


def index(request):
    """
    Home page view.
    Displays welcome message and upload form.
    """
    context = {
        'title': 'Resume Analyzer',
        'description': 'Upload your resume and enter a job description to see how well your qualifications match the position.'
    }
    return render(request, 'analyzer/index.html', context)


def analyze(request):
    """
    Handle resume upload and job description input.
    Performs ML analysis and displays results.
    """
    if request.method == 'POST':
        form = ResumeAnalysisForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Get form data
                resume_file = request.FILES['resume_file']
                job_description = form.cleaned_data['job_description']
                
                # Initialize analyzer
                analyzer = ResumeAnalyzer()
                
                # Analyze resume
                analysis_results = analyzer.analyze_resume(resume_file, job_description)
                
                # Save to database
                analysis = ResumeAnalysis.objects.create(
                    resume_file=resume_file,
                    resume_text=analysis_results['resume_text'],
                    job_description=job_description,
                    match_score=analysis_results['match_score'],
                    matched_skills=','.join(analysis_results['matched_skills']),
                    missing_skills=','.join(analysis_results['missing_skills'])
                )
                
                # Redirect to results page
                return redirect('results', pk=analysis.pk)
                
            except Exception as e:
                messages.error(request, f'Error during analysis: {str(e)}')
                return render(request, 'analyzer/analyze.html', {'form': form})
    else:
        form = ResumeAnalysisForm()
    
    context = {
        'form': form,
        'title': 'Analyze Resume'
    }
    return render(request, 'analyzer/analyze.html', context)


def results(request, pk):
    """
    Display analysis results.
    Shows match score, matched skills, and missing skills.
    """
    try:
        analysis = ResumeAnalysis.objects.get(pk=pk)
        
        # Get skills lists
        matched_skills = analysis.get_matched_skills_list()
        missing_skills = analysis.get_missing_skills_list()
        
        # Determine recommendation
        match_score = analysis.match_score
        if match_score >= 80:
            recommendation = "Excellent fit! Your qualifications strongly align with this position."
            recommendation_class = "success"
        elif match_score >= 60:
            recommendation = "Good match! You have most of the required skills."
            recommendation_class = "info"
        elif match_score >= 40:
            recommendation = "Fair match. Consider developing some additional skills."
            recommendation_class = "warning"
        else:
            recommendation = "This position may not be the best fit for your current skills."
            recommendation_class = "danger"
        
        context = {
            'analysis': analysis,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'recommendation': recommendation,
            'recommendation_class': recommendation_class,
            'title': 'Analysis Results'
        }
        
        return render(request, 'analyzer/results.html', context)
        
    except ResumeAnalysis.DoesNotExist:
        messages.error(request, 'Analysis not found.')
        return redirect('index')