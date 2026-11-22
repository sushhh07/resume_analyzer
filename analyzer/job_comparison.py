
from .job_roles import JOB_ROLES
from .ml_utils import ResumeAnalyzer


def compare_job_roles(resume_text, selected_roles):

    analyzer = ResumeAnalyzer()

    # Extract skills from resume
    resume_skills = set(analyzer.extract_skills(resume_text))

    comparison_results = []

    for role in selected_roles:

        if role not in JOB_ROLES:
            continue

        required_skills = set(
            JOB_ROLES[role]["skills"]
        )

        matched_skills = list(
            resume_skills.intersection(required_skills)
        )

        missing_skills = list(
            required_skills - resume_skills
        )

        if required_skills:
            match_score = round(
                (len(matched_skills) / len(required_skills)) * 100,
                2
            )
        else:
            match_score = 0

        comparison_results.append({
            "role": role,
            "description": JOB_ROLES[role]["description"],
            "match_score": match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    # Sort roles by highest match score
    comparison_results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return comparison_results

