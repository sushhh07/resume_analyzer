"""
URL Configuration for the analyzer app.
Routes:
- / : Home page
- /analyze/ : Resume upload and analysis
- /results/<id>/ : Display results
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze, name='analyze'),
    path('results/<int:pk>/', views.results, name='results'),
    path('compare-roles/', views.compare_roles, name='compare_roles'),
    path('history/', views.analysis_history, name='analysis_history'),
    path('report/<int:pk>/', views.download_report, name='download_report'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]