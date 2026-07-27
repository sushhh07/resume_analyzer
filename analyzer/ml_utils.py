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
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import numpy as np


class ResumeAnalyzer:
    """
    Main class for analyzing resumes and calculating match scores.
    """
    
    def __init__(self):
        """
        Initialize the analyzer with TF-IDF vectorizer.
        """
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            min_df=1,
            max_df=0.95,
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2)  # Include unigrams and bigrams
        )
    
    def extract_text_from_pdf(self, pdf_file):
        """
        Extract text from a PDF file using PyMuPDF.
        
        Args:
            pdf_file: File object or path to PDF file
            
        Returns:
            str: Extracted text from PDF
            
        Raises:
            Exception: If PDF reading fails
        """
        try:
            # Handle file objects
            if hasattr(pdf_file, 'read'):
                # It's a file object, read bytes
                pdf_bytes = pdf_file.read()
                pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            else:
                # It's a file path
                pdf_document = fitz.open(pdf_file)
            
            extracted_text = ""
            
            # Extract text from all pages
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                extracted_text += page.get_text()
            
            pdf_document.close()
            return extracted_text
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def preprocess_text(self, text):
        """
        Preprocess text by:
        - Converting to lowercase
        - Removing special characters and punctuation
        - Removing extra whitespace
        - Removing stop words (using scikit-learn's stop words)
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and keep only alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_skills(self, text, num_skills=20):
        """
        Extract important skills/keywords from text using TF-IDF.
        
        Args:
            text: Text to extract skills from
            num_skills: Number of top skills to extract
            
        Returns:
            list: List of extracted skills sorted by importance
        """
        # Preprocess the text
        processed_text = self.preprocess_text(text)
        
        # Split into words and filter by length
        words = [word for word in processed_text.split() if len(word) > 2]
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top skills
        sorted_skills = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        skills = [skill[0] for skill in sorted_skills[:num_skills]]
        
        return skills
    
    def calculate_match_score(self, resume_text, job_description):
        """
        Calculate match score between resume and job description.
        Uses TF-IDF vectorization and cosine similarity.
        
        Args:
            resume_text: Extracted text from resume
            job_description: Job description text
            
        Returns:
            tuple: (match_score (0-100), matched_skills (list), missing_skills (list))
        """
        try:
            # Preprocess both texts
            resume_processed = self.preprocess_text(resume_text)
            job_processed = self.preprocess_text(job_description)
            
            # Vectorize texts using TF-IDF
            # We need to fit on both documents together
            texts = [resume_processed, job_processed]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage (0-100)
            match_score = round(float(similarity) * 100, 2)
            
            # Extract skills from both documents
            resume_skills = set(self.extract_skills(resume_text, num_skills=30))
            job_skills = set(self.extract_skills(job_description, num_skills=30))
            
            # Find matched and missing skills
            matched_skills = resume_skills.intersection(job_skills)
            missing_skills = job_skills - resume_skills
            
            return {
                'match_score': match_score,
                'matched_skills': sorted(list(matched_skills)),
                'missing_skills': sorted(list(missing_skills))
            }
            
        except Exception as e:
            raise Exception(f"Error calculating match score: {str(e)}")
    
    def analyze_resume(self, pdf_file, job_description):
        """
        Complete pipeline to analyze resume against job description.
        
        Args:
            pdf_file: Uploaded PDF file
            job_description: Job description text
            
        Returns:
            dict: Analysis results including:
                - resume_text: Extracted text
                - match_score: Match percentage
                - matched_skills: Skills found in both
                - missing_skills: Skills missing from resume
        """
        try:
            # Step 1: Extract text from PDF
            resume_text = self.extract_text_from_pdf(pdf_file)
            
            # Step 2: Calculate match score
            results = self.calculate_match_score(resume_text, job_description)
            
            # Add resume text to results
            results['resume_text'] = resume_text
            
            return results
            
        except Exception as e:
            raise Exception(f"Error during resume analysis: {str(e)}")