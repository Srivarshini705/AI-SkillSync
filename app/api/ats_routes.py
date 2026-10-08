from fastapi import APIRouter, HTTPException

from app.models.ats_models import (
    ATSAnalyzeRequest,
    ATSAnalyzeResponse,
    ATSJobAnalyzeRequest,
    ATSJobAnalyzeResponse,
)
from app.services.ats_analyzer import (
    analyze_resume_against_job,
    analyze_resume_with_llm,
)
from app.services.llm_service import LLMServiceError


router = APIRouter(
    prefix="/api/ats",
    tags=["ATS Analysis"],
)


@router.post(
    "/analyze",
    response_model=ATSAnalyzeResponse,
)
async def analyze_resume(
    request: ATSAnalyzeRequest,
) -> ATSAnalyzeResponse:
    """
    Perform general ATS analysis on a resume.
    """

    try:
        result = analyze_resume_with_llm(
            resume_text=request.resume_text,
            skills=request.skills,
            experience=request.experience,
            projects=request.projects,
            education=request.education,
            achievements=request.achievements,
        )

        return ATSAnalyzeResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except LLMServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail="ATS semantic analysis service is unavailable.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal ATS analysis error.",
        ) from exc


@router.post(
    "/analyze-job",
    response_model=ATSJobAnalyzeResponse,
)
async def analyze_resume_for_job(
    request: ATSJobAnalyzeRequest,
) -> ATSJobAnalyzeResponse:
    """
    Analyze a resume against a specific job description.
    """

    try:
        result = analyze_resume_against_job(
            resume_text=request.resume_text,
            job_description=request.job_description,
            skills=request.skills,
            experience=request.experience,
            projects=request.projects,
            education=request.education,
            achievements=request.achievements,
        )

        return ATSJobAnalyzeResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except LLMServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail="ATS semantic analysis service is unavailable.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal ATS analysis error.",
        ) from exc