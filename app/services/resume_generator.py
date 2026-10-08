from typing import Any

from app.models.resume_models import ResumeData
from app.prompts.resume_prompts import (
    RESUME_GENERATION_SYSTEM_PROMPT,
    build_resume_generation_prompt,
)
from app.services.llm_service import LLMService


class ResumeGenerationError(Exception):
    """Raised when resume generation fails."""


def generate_resume(
    resume_data: ResumeData,
    llm_service: LLMService | None = None,
) -> ResumeData:
    """
    Generate professionally improved resume content using Groq.

    The LLM is only allowed to improve the wording of information
    already provided by the candidate.
    """

    service = llm_service or LLMService()

    user_prompt = build_resume_generation_prompt(
        name=resume_data.name,
        email=str(resume_data.email) if resume_data.email else None,
        phone=resume_data.phone,
        summary=resume_data.summary,
        education=resume_data.education,
        skills=resume_data.skills,
        projects=resume_data.projects,
        experience=resume_data.experience,
        certifications=resume_data.certifications,
        achievements=resume_data.achievements,
    )

    try:
        result: dict[str, Any] = service.generate_json(
            system_prompt=RESUME_GENERATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
    except Exception as exc:
        raise ResumeGenerationError(
            "Unable to generate resume content."
        ) from exc

    try:
        return ResumeData(**result)
    except Exception as exc:
        raise ResumeGenerationError(
            "Groq returned invalid resume data."
        ) from exc