from app.services.ats_analyzer import (
    calculate_ats_score,
    match_keywords,
)

from app.models.ats_models import (
    ATSAnalyzeRequest,
    ATSAnalyzeResponse,
    ATSComponentScores,
    ATSJobAnalyzeRequest,
    ATSJobAnalyzeResponse,
)


def test_keyword_matching():
    resume = """
    Python FastAPI Machine Learning
    """

    job_description = """
    Looking for Python FastAPI developers with Docker experience.
    """

    result = match_keywords(resume, job_description)

    assert "python" in result["matched_keywords"]
    assert "fastapi" in result["matched_keywords"]
    assert "docker" in result["missing_keywords"]


def test_ats_score_with_complete_resume():
    resume = """
    John Doe

    Professional Summary
    Computer Science developer.

    Skills
    Python, FastAPI, Machine Learning

    Experience
    Software Developer

    Projects
    AI Resume Analyzer

    Education
    B.Tech Computer Science

    Achievements
    Hackathon Winner
    """

    result = calculate_ats_score(
        resume,
        skills=["Python", "FastAPI", "Machine Learning"],
        experience=["Software Developer"],
        projects=["AI Resume Analyzer"],
        education=["B.Tech Computer Science"],
        achievements=["Hackathon Winner"],
    )

    assert 0 <= result["ats_score"] <= 100

    assert result["component_scores"]["skills"] == 100
    assert result["component_scores"]["experience"] == 100
    assert result["component_scores"]["projects"] == 100
    assert result["component_scores"]["education"] == 100
    assert result["component_scores"]["achievements"] == 100


def test_job_specific_ats_matching():
    resume = """
    Skills
    Python, FastAPI, Machine Learning

    Projects
    AI Application

    Education
    B.Tech Computer Science
    """

    job_description = """
    Python FastAPI Docker Machine Learning developer.
    """

    result = calculate_ats_score(
        resume,
        skills=["Python", "FastAPI", "Machine Learning"],
        projects=["AI Application"],
        education=["B.Tech Computer Science"],
        job_description=job_description,
    )

    assert 0 <= result["ats_score"] <= 100
    assert "python" in result["matched_keywords"]
    assert "docker" in result["missing_keywords"]


def test_empty_resume_raises_error():
    try:
        calculate_ats_score("")
        assert False
    except ValueError:
        assert True
def test_ats_request_model():
    request = ATSAnalyzeRequest(
        resume_text="Python developer with FastAPI experience.",
        skills=["Python", "FastAPI"],
        experience=["Software Developer"],
        projects=["AI Project"],
        education=["B.Tech Computer Science"],
    )

    assert request.resume_text
    assert "Python" in request.skills


def test_job_ats_request_model():
    request = ATSJobAnalyzeRequest(
        resume_text="Python developer with FastAPI experience.",
        skills=["Python", "FastAPI"],
        job_description="Looking for a Python FastAPI developer.",
    )

    assert request.job_description
    assert "Python" in request.skills


def test_ats_response_model():
    response = ATSAnalyzeResponse(
        ats_score=85.5,
        component_scores=ATSComponentScores(
            skills=90,
            keywords=85,
            experience=80,
            projects=90,
            education=100,
            achievements=70,
            formatting=90,
        ),
        matched_keywords=["python", "fastapi"],
        missing_keywords=["docker"],
        missing_skills=["Docker"],
        suggestions=["Add Docker if applicable."],
        summary="Strong ATS compatibility.",
    )

    assert response.ats_score == 85.5
    assert response.component_scores.skills == 90
    assert "docker" in response.missing_keywords


def test_job_ats_response_model():
    response = ATSJobAnalyzeResponse(
        ats_score=80,
        component_scores=ATSComponentScores(
            skills=80,
            keywords=80,
            experience=80,
            projects=80,
            education=80,
            achievements=80,
            formatting=80,
        ),
        job_match_summary="Good match for the target role.",
    )

    assert response.ats_score == 80
    assert response.job_match_summary      
