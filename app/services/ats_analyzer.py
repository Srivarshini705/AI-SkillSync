import re
from typing import Any

from app.prompts.ats_prompts import (
    GENERAL_ATS_SYSTEM_PROMPT,
    JOB_ATS_SYSTEM_PROMPT,
    build_general_ats_prompt,
    build_job_ats_prompt,
)
from app.services.llm_service import LLMService


ATS_WEIGHTS = {
    "skills": 20,
    "keywords": 20,
    "experience": 15,
    "projects": 15,
    "education": 10,
    "achievements": 10,
    "formatting": 10,
}


def _normalize_text(text: str) -> str:
    """Normalize text for reliable keyword matching."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _calculate_percentage(found: int, total: int) -> float:
    """Calculate a percentage safely."""
    if total <= 0:
        return 100.0

    return round((found / total) * 100, 2)


def _score_section(present: bool) -> float:
    """Return 100 if a section exists, otherwise 0."""
    return 100.0 if present else 0.0


def extract_keywords(text: str) -> set[str]:
    """
    Extract simple ATS-friendly keywords from text.
    """

    normalized = _normalize_text(text)

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#.-]{1,}\b",
        normalized,
    )

    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "this",
        "that",
        "have",
        "has",
        "are",
        "was",
        "were",
        "will",
        "your",
        "you",
        "our",
        "their",
        "about",
        "into",
        "using",
        "used",
        "work",
        "working",
        "experience",
        "years",
        "year",
        "job",
        "role",
        "team",
        "candidate",
    }

    return {
        word
        for word in words
        if word not in stop_words and len(word) >= 2
    }


def match_keywords(
    resume_text: str,
    job_description: str,
) -> dict[str, list[str]]:
    """
    Compare resume keywords against job-description keywords.
    """

    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    matched = sorted(resume_keywords & job_keywords)
    missing = sorted(job_keywords - resume_keywords)

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
    }


def calculate_formatting_score(resume_text: str) -> float:
    """
    Apply basic deterministic ATS-friendly formatting checks.
    """

    score = 100.0

    lines = [
        line.strip()
        for line in resume_text.split("\n")
        if line.strip()
    ]

    if not lines:
        return 0.0

    long_lines = sum(
        len(line) > 180
        for line in lines
    )

    if long_lines:
        score -= min(long_lines * 5, 20)

    section_patterns = [
        r"\bsummary\b",
        r"\beducation\b",
        r"\bskills\b",
        r"\bexperience\b",
        r"\bprojects?\b",
    ]

    detected_sections = sum(
        bool(re.search(pattern, resume_text, re.IGNORECASE))
        for pattern in section_patterns
    )

    if detected_sections < 3:
        score -= 20

    if re.search(
        r"[!]{3,}|[?]{3,}|[.]{5,}",
        resume_text,
    ):
        score -= 10

    return max(round(score, 2), 0.0)


def calculate_ats_score(
    resume_text: str,
    *,
    skills: list[str] | None = None,
    experience: list[str] | None = None,
    projects: list[str] | None = None,
    education: list[str] | None = None,
    achievements: list[str] | None = None,
    job_description: str | None = None,
) -> dict[str, Any]:
    """
    Calculate the deterministic ATS score.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    normalized_resume = _normalize_text(resume_text)

    skills = skills or []
    experience = experience or []
    projects = projects or []
    education = education or []
    achievements = achievements or []

    # Skills
    if job_description:
        skill_matches = 0
        normalized_jd = _normalize_text(job_description)

        for skill in skills:
            if _normalize_text(skill) in normalized_jd:
                skill_matches += 1

        skills_score = _calculate_percentage(
            skill_matches,
            len(skills),
        )
    else:
        skills_score = _score_section(bool(skills))

    # Keywords
    if job_description:
        keyword_result = match_keywords(
            resume_text,
            job_description,
        )

        total_jd_keywords = (
            len(keyword_result["matched_keywords"])
            + len(keyword_result["missing_keywords"])
        )

        keywords_score = _calculate_percentage(
            len(keyword_result["matched_keywords"]),
            total_jd_keywords,
        )
    else:
        keyword_result = {
            "matched_keywords": [],
            "missing_keywords": [],
        }

        keywords_score = 100.0

    # Other components
    experience_score = _score_section(bool(experience))
    projects_score = _score_section(bool(projects))
    education_score = _score_section(bool(education))
    achievements_score = _score_section(bool(achievements))

    formatting_score = calculate_formatting_score(
        normalized_resume
    )

    component_scores = {
        "skills": round(skills_score, 2),
        "keywords": round(keywords_score, 2),
        "experience": round(experience_score, 2),
        "projects": round(projects_score, 2),
        "education": round(education_score, 2),
        "achievements": round(achievements_score, 2),
        "formatting": round(formatting_score, 2),
    }

    weighted_score = sum(
        component_scores[name] * (weight / 100)
        for name, weight in ATS_WEIGHTS.items()
    )

    return {
        "ats_score": round(weighted_score, 2),
        "component_scores": component_scores,
        "matched_keywords": keyword_result["matched_keywords"],
        "missing_keywords": keyword_result["missing_keywords"],
    }


def analyze_resume_with_llm(
    resume_text: str,
    *,
    skills: list[str] | None = None,
    experience: list[str] | None = None,
    projects: list[str] | None = None,
    education: list[str] | None = None,
    achievements: list[str] | None = None,
    llm_service: LLMService | None = None,
) -> dict[str, Any]:
    """
    Perform general ATS analysis using deterministic Python
    scoring plus Groq semantic analysis.
    """

    deterministic_result = calculate_ats_score(
        resume_text,
        skills=skills,
        experience=experience,
        projects=projects,
        education=education,
        achievements=achievements,
    )

    service = llm_service or LLMService()

    llm_result = service.generate_json(
        system_prompt=GENERAL_ATS_SYSTEM_PROMPT,
        user_prompt=build_general_ats_prompt(resume_text),
    )

    return {
        **deterministic_result,
        "missing_skills": _ensure_string_list(
            llm_result.get("missing_skills", [])
        ),
        "suggestions": _ensure_string_list(
            llm_result.get("suggestions", [])
        ),
        "summary": _ensure_string(
            llm_result.get("summary", "")
        ),
    }


def analyze_resume_against_job(
    resume_text: str,
    job_description: str,
    *,
    skills: list[str] | None = None,
    experience: list[str] | None = None,
    projects: list[str] | None = None,
    education: list[str] | None = None,
    achievements: list[str] | None = None,
    llm_service: LLMService | None = None,
) -> dict[str, Any]:
    """
    Perform job-specific ATS analysis.

    Python calculates the numerical ATS score and keyword matching.
    Groq provides semantic analysis and recommendations.
    """

    if not job_description or not job_description.strip():
        raise ValueError(
            "Job description cannot be empty."
        )

    deterministic_result = calculate_ats_score(
        resume_text,
        skills=skills,
        experience=experience,
        projects=projects,
        education=education,
        achievements=achievements,
        job_description=job_description,
    )

    service = llm_service or LLMService()

    llm_result = service.generate_json(
        system_prompt=JOB_ATS_SYSTEM_PROMPT,
        user_prompt=build_job_ats_prompt(
            resume_text=resume_text,
            job_description=job_description,
            matched_keywords=deterministic_result[
                "matched_keywords"
            ],
            missing_keywords=deterministic_result[
                "missing_keywords"
            ],
        ),
    )

    return {
        **deterministic_result,
        "missing_skills": _ensure_string_list(
            llm_result.get("missing_skills", [])
        ),
        "suggestions": _ensure_string_list(
            llm_result.get("suggestions", [])
        ),
        "summary": _ensure_string(
            llm_result.get("summary", "")
        ),
        "job_match_summary": _ensure_string(
            llm_result.get("job_match_summary", "")
        ),
    }


def _ensure_string_list(value: Any) -> list[str]:
    """Safely convert an LLM list response into strings."""

    if not isinstance(value, list):
        return []

    return [
        str(item).strip()
        for item in value
        if str(item).strip()
    ]


def _ensure_string(value: Any) -> str:
    """Safely convert an LLM response field into a string."""

    if value is None:
        return ""

    return str(value).strip()