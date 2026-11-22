"""
Machine Learning Utilities for Resume Analysis.

This module contains functions for:
- Text extraction from PDF files (PyMuPDF)
- Text preprocessing (lowercase, remove punctuation, remove stop words)
- TF-IDF Vectorization
- Cosine Similarity calculation
- Skills extraction and matching

Key Functions:
- extract_text_from_pdf(file_path): Extract text from PDF
- preprocess_text(text): Clean and normalize text
- calculate_match_score(resume_text, job_description): Calculate similarity score
- extract_skills(text): Extract keywords/skills from text
"""

import re
import fitz

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .skill_categories import SKILL_CATEGORIES

class ResumeAnalyzer:

    def __init__(self):

        self.skills = [
            "python",
            "django",
            "html",
            "css",
            "javascript",
            "java",
            "c",
            "c++",
            "sql",
            "mysql",
            "bootstrap",
            "react",
            "git",
            "github",
            "api",
            "sqlite",
            "machine learning",
            "tensorflow",
            "numpy",
            "pandas",
            "excel"
        ]

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

    def extract_text_from_pdf(self, pdf_file):

        pdf_bytes = pdf_file.read()

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        return text
            
        
    
    def preprocess_text(self, text):

        text = text.lower()

        text = re.sub(r'[^a-z0-9 ]', ' ', text)

        text = re.sub(r'\s+', ' ', text)

        return text
    
    

    def extract_skills(self, text):

        text = re.sub(r'\s+', ' ', text.lower())

        found_skills = []

        skills_sorted = sorted(
            self.skills,
            key=len,
            reverse=True
        )

        for skill in skills_sorted:

            skill_pattern = re.escape(skill.lower())

            if skill.lower() == "c":
                skill_pattern = r'c(?![+#])'

            pattern = (
                r'(?<![a-z0-9])'
                + skill_pattern
                + r'(?![a-z0-9])'
            )

            if re.search(pattern, text):
                found_skills.append(skill)

        return found_skills
    
    def categorize_skills(self, skills):

        categorized = {}

        for category, category_skills in SKILL_CATEGORIES.items():

            matched = [
                skill for skill in skills
                if skill in category_skills
            ]

            if matched:
                categorized[category] = matched

        return categorized



    
    def calculate_match_score(self, resume_text, job_description):

        resume_processed = self.preprocess_text(resume_text)
        job_processed = self.preprocess_text(job_description)

        tfidf = self.vectorizer.fit_transform(
           [resume_processed, job_processed]
        )

        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]


        resume_skills = set(self.extract_skills(resume_text))
        job_skills = set(self.extract_skills(job_description))

        matched_skills = list(resume_skills.intersection(job_skills))
        missing_skills = list(job_skills - resume_skills)
        matched_categories = self.categorize_skills(matched_skills)
        missing_categories = self.categorize_skills(missing_skills)

        if len(job_skills) > 0:
           match_score = round((len(matched_skills) / len(job_skills)) * 100, 2)
        else:
           match_score = 0

        print("Similarity :", similarity)
        print("Match Score :", match_score)
        print("Matched Skills :", matched_skills)
        print("Missing Skills :", missing_skills)

        return {
           "match_score": match_score,
           "matched_skills": matched_skills,
           "missing_skills": missing_skills,
           "matched_categories": matched_categories,
           "missing_categories": missing_categories
        }
    def analyze_resume(self, pdf_file, job_description):
          """
          Complete resume analysis.
          """

          resume_text = self.extract_text_from_pdf(pdf_file)

          result = self.calculate_match_score(
             resume_text,
             job_description
          )

          result["resume_text"] = resume_text

          return result