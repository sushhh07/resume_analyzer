"""
Views for the Resume Analyzer application.

Views:
- index: Home page
- analyze: Handle resume upload and analysis
- results: Display analysis results
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from xml.sax.saxutils import escape

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ResumeAnalysisForm
from .models import ResumeAnalysis
from .ml_utils import ResumeAnalyzer
from .resume_quality import check_resume_quality
from .job_roles import JOB_ROLES
from .job_comparison import compare_job_roles



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

@login_required
def analyze(request):
    """
    Handle resume upload and job description input.
    Performs ML analysis and displays results.
    """
    if request.method == 'POST':
        form = ResumeAnalysisForm(request.POST, request.FILES)
        print("POST:", request.POST)
        print("FILES:", request.FILES)

        if form.is_valid():
            print("Form is valid")
            try:
                # Get form data
                resume_file = request.FILES['resume_file']
                print("Resume File:", resume_file)
                job_description = form.cleaned_data['job_description']
                
                # Initialize analyzer
                analyzer = ResumeAnalyzer()
                
                # Analyze resume
                analysis_results = analyzer.analyze_resume(resume_file, job_description)
                

                print("Resume Text:")
                print(analysis_results['resume_text'])

                print("Job Description:")
                print(job_description)

                print("Match Score:")
                print(analysis_results['match_score'])

                print("Matched Skills:")
                print(analysis_results['matched_skills'])

                print("Missing Skills:")
                print(analysis_results['missing_skills'])
                # Save to database
                analysis = ResumeAnalysis.objects.create(
                  
    user=request.user,
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

@login_required
def results(request, pk):
    """
    Display analysis results.
    Shows match score, matched skills, and missing skills.
    """
    try:
        analysis = ResumeAnalysis.objects.get(pk=pk)
        # Check resume quality
        quality_results = check_resume_quality(analysis.resume_text)
        
        # Get skills lists
        matched_skills = analysis.get_matched_skills_list()
        missing_skills = analysis.get_missing_skills_list()
        total_skills = len(matched_skills) + len(missing_skills)
        # Categorize matched and missing skills
        analyzer = ResumeAnalyzer()

        matched_categories = analyzer.categorize_skills(matched_skills)
        missing_categories = analyzer.categorize_skills(missing_skills)
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
            'matched_categories': matched_categories,
            'missing_categories': missing_categories,
            'total_skills': total_skills,
            'recommendation': recommendation,
            'recommendation_class': recommendation_class,
            
            'quality_score': quality_results['quality_score'],
            'quality_sections': quality_results['sections'],
            'missing_sections': quality_results['missing_sections'],
            'title': 'Analysis Results'
        }
        
        return render(request, 'analyzer/results.html', context)
    


        
    except ResumeAnalysis.DoesNotExist:
        messages.error(request, 'Analysis not found.')
        return redirect('index')
    
def compare_roles(request):

    if request.method == 'POST':

        resume_file = request.FILES.get('resume_file')
        selected_roles = request.POST.getlist('job_roles')

        if not resume_file:
            messages.error(request, 'Please upload your resume.')
            return redirect('compare_roles')

        if not selected_roles:
            messages.error(request, 'Please select at least one job role.')
            return redirect('compare_roles')

        try:
            analyzer = ResumeAnalyzer()

            resume_text = analyzer.extract_text_from_pdf(
                resume_file
            )

            comparison_results = compare_job_roles(
                resume_text,
                selected_roles
            )

            context = {
                'comparison_results': comparison_results,
                'title': 'Job Role Comparison'
            }

            return render(
                request,
                'analyzer/job_comparison_results.html',
                context
            )

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('compare_roles')

    context = {
        'job_roles': JOB_ROLES,
        'title': 'Compare Job Roles'
    }

    return render(
        request,
        'analyzer/compare_roles.html',
        context
    )
@login_required
def analysis_history(request):
    analyses = ResumeAnalysis.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {
        'analyses': analyses,
        'title': 'Analysis History'
    }

    return render(request, 'analyzer/analysis_history.html', context)
@login_required
def download_report(request, pk):
    analysis = get_object_or_404(
    ResumeAnalysis,
    pk=pk,
    user=request.user
)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="resume_analysis_{pk}.pdf"'
    )

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Resume Analysis Report", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(
        f"<b>Match Score:</b> {analysis.match_score}%",
        styles['Normal']
    ))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "<b>Job Description:</b>",
        styles['Heading2']
    ))
    content.append(Paragraph(
        escape(analysis.job_description).replace('\n', '<br/>'),
        styles['Normal']
    ))
    content.append(Spacer(1, 15))

    content.append(Paragraph(
        "<b>Matched Skills:</b>",
        styles['Heading2']
    ))
    content.append(Paragraph(
        escape(analysis.matched_skills or "No matched skills"),
        styles['Normal']
    ))
    content.append(Spacer(1, 15))

    content.append(Paragraph(
        "<b>Missing Skills:</b>",
        styles['Heading2']
    ))
    content.append(Paragraph(
        escape(analysis.missing_skills or "No missing skills"),
        styles['Normal']
    ))
    content.append(Spacer(1, 15))

    quality = check_resume_quality(analysis.resume_text)

    content.append(Paragraph(
        f"<b>Resume Quality Score:</b> {quality['quality_score']}%",
        styles['Normal']
    ))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "<b>Missing Resume Sections:</b>",
        styles['Heading2']
    ))

    missing = quality['missing_sections']
    missing_text = ", ".join(missing) if missing else "None"

    content.append(Paragraph(
        escape(missing_text),
        styles['Normal']
    ))

    pdf.build(content)

    response.write(buffer.getvalue())
    buffer.close()

    return response
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'analyzer/signup.html', {
        'form': form
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'analyzer/login.html')
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')