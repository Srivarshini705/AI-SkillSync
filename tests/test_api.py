from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "member3-resume-ats"


def test_resume_create_endpoint(monkeypatch):
    def fake_generate_resume(resume_data):
        return resume_data

    monkeypatch.setattr(
        "app.api.resume_routes.generate_resume",
        fake_generate_resume,
    )

    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+91 9876543210",
        "summary": "Computer Science student interested in AI.",
        "education": [
            "B.Tech Computer Science"
        ],
        "skills": [
            "Python",
            "FastAPI",
            "Machine Learning"
        ],
        "projects": [
            "AI Resume Analyzer"
        ],
        "experience": [
            "Software Developer Intern"
        ],
        "certifications": [],
        "achievements": [
            "Hackathon Winner"
        ],
    }

    response = client.post(
        "/api/resume/create",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "Python" in data["skills"]


def test_ats_analyze_endpoint(monkeypatch):
    def fake_analyze_resume_with_llm(**kwargs):
        return {
            "ats_score": 85.0,
            "component_scores": {
                "skills": 90,
                "keywords": 85,
                "experience": 80,
                "projects": 85,
                "education": 90,
                "achievements": 70,
                "formatting": 90,
            },
            "matched_keywords": [
                "Python",
                "FastAPI",
            ],
            "missing_keywords": [
                "Docker",
            ],
            "missing_skills": [
                "Docker",
            ],
            "suggestions": [
                "Add Docker experience if applicable."
            ],
            "summary": "Good technical foundation.",
        }

    monkeypatch.setattr(
        "app.api.ats_routes.analyze_resume_with_llm",
        fake_analyze_resume_with_llm,
    )

    payload = {
        "resume_text": (
            "Computer Science student with Python "
            "and FastAPI experience."
        ),
        "skills": [
            "Python",
            "FastAPI",
        ],
        "experience": [
            "Software Developer Intern"
        ],
        "projects": [
            "AI Resume Analyzer"
        ],
        "education": [
            "B.Tech Computer Science"
        ],
        "achievements": [],
    }

    response = client.post(
        "/api/ats/analyze",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ats_score"] == 85.0
    assert "Python" in data["matched_keywords"]
    assert "Docker" in data["missing_skills"]


def test_ats_analyze_job_endpoint(monkeypatch):
    def fake_analyze_resume_against_job(**kwargs):
        return {
            "ats_score": 78.0,
            "component_scores": {
                "skills": 80,
                "keywords": 75,
                "experience": 80,
                "projects": 75,
                "education": 90,
                "achievements": 70,
                "formatting": 85,
            },
            "matched_keywords": [
                "Python",
                "FastAPI",
            ],
            "missing_keywords": [
                "Docker",
                "AWS",
            ],
            "missing_skills": [
                "Docker",
                "AWS",
            ],
            "suggestions": [
                "Add Docker and AWS experience if applicable."
            ],
            "summary": "Partial match for the backend role.",
            "job_match_summary": (
                "The resume matches Python and FastAPI "
                "requirements but lacks several cloud "
                "and containerization keywords."
            ),
        }

    monkeypatch.setattr(
        "app.api.ats_routes.analyze_resume_against_job",
        fake_analyze_resume_against_job,
    )

    payload = {
        "resume_text": (
            "Computer Science student with Python "
            "and FastAPI experience."
        ),
        "skills": [
            "Python",
            "FastAPI",
        ],
        "experience": [
            "Software Developer Intern"
        ],
        "projects": [
            "AI Resume Analyzer"
        ],
        "education": [
            "B.Tech Computer Science"
        ],
        "achievements": [],
        "job_description": (
            "Python Backend Developer with FastAPI, "
            "Docker, AWS and REST API experience."
        ),
    }

    response = client.post(
        "/api/ats/analyze-job",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ats_score"] == 78.0
    assert "Python" in data["matched_keywords"]
    assert "Docker" in data["missing_skills"]
    assert data["job_match_summary"]


def test_resume_upload_rejects_non_pdf():
    response = client.post(
        "/api/resume/upload",
        files={
            "file": (
                "resume.txt",
                b"This is not a PDF.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]