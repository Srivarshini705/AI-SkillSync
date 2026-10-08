from app.services.resume_parser import parse_resume_text


def test_parse_complete_resume():
    text = """
    JOHN DOE
    john@example.com
    +91 9876543210

    SUMMARY
    Computer Science student interested in AI.

    EDUCATION
    B.Tech Computer Science - ABC University

    SKILLS
    Python, FastAPI, SQL, Machine Learning

    PROJECTS
    AI Resume Analyzer
    Chatbot Application

    EXPERIENCE
    Software Engineering Intern - ABC Technologies

    CERTIFICATIONS
    Python Certificate

    ACHIEVEMENTS
    Hackathon Winner
    """

    resume = parse_resume_text(text)

    assert resume.name == "JOHN DOE"
    assert resume.email == "john@example.com"
    assert resume.phone is not None

    assert "Python" in resume.skills
    assert "FastAPI" in resume.skills

    assert len(resume.education) == 1
    assert len(resume.projects) == 2
    assert len(resume.experience) == 1
    assert len(resume.certifications) == 1
    assert len(resume.achievements) == 1


def test_parse_resume_with_missing_sections():
    text = """
    JANE DOE
    jane@example.com

    SKILLS
    Python, SQL

    EDUCATION
    B.Tech Computer Science
    """

    resume = parse_resume_text(text)

    assert resume.name == "JANE DOE"
    assert resume.email == "jane@example.com"

    assert "Python" in resume.skills
    assert "SQL" in resume.skills

    assert resume.projects == []
    assert resume.experience == []
    assert resume.certifications == []
    assert resume.achievements == []


def test_empty_resume_raises_error():
    try:
        parse_resume_text("")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "empty" in str(exc).lower()


def test_different_section_names():
    text = """
    JOHN SMITH
    john@example.com

    PROFESSIONAL PROFILE
    Software developer with Python experience.

    TECHNICAL SKILLS
    Python | FastAPI | Docker | Git

    WORK EXPERIENCE
    Backend Developer Intern

    ACADEMIC BACKGROUND
    B.Tech Computer Science
    """

    resume = parse_resume_text(text)

    assert resume.summary is not None
    assert "Python" in resume.skills
    assert "FastAPI" in resume.skills
    assert len(resume.experience) == 1
    assert len(resume.education) == 1