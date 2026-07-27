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
]