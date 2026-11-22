
import re


def check_resume_quality(resume_text):

    text = resume_text.lower()

    sections = {
        "Contact Information": bool(
            re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
            or re.search(r'\b\d{10}\b', text)
        ),

        "Education": any(
            word in text for word in
            ["education", "b.tech", "bachelor", "degree", "university"]
        ),

        "Skills": any(
            word in text for word in
            ["skills", "technical skills", "programming"]
        ),

        "Projects": any(
            word in text for word in
            ["projects", "project"]
        ),

        "Experience / Internship": any(
            word in text for word in
            ["experience", "internship", "work experience"]
        ),

        "Professional Summary": any(
            word in text for word in
            ["summary", "objective", "profile"]
        ),

        "Certifications": any(
            word in text for word in
            ["certifications", "certificates", "certification"]
        )
    }

    total_sections = len(sections)
    completed_sections = sum(sections.values())

    quality_score = round(
        (completed_sections / total_sections) * 100
    )

    missing_sections = [
        name for name, present in sections.items()
        if not present
    ]

    return {
        "quality_score": quality_score,
        "sections": sections,
        "missing_sections": missing_sections
    }
