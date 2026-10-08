from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.resume_models import ResumeData
from app.services.pdf_service import extract_text_from_pdf
from app.services.resume_generator import (
    ResumeGenerationError,
    generate_resume,
)
from app.services.resume_parser import parse_resume_text


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"],
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post(
    "/create",
    response_model=ResumeData,
)
async def create_resume(
    request: ResumeData,
) -> ResumeData:
    """
    Generate professionally improved resume content
    from candidate-provided information.
    """

    try:
        return generate_resume(request)

    except ResumeGenerationError as exc:
        raise HTTPException(
            status_code=502,
            detail="Resume generation service is unavailable.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal resume generation error.",
        ) from exc


@router.post(
    "/upload",
    response_model=ResumeData,
)
async def upload_resume(
    file: UploadFile = File(...),
) -> ResumeData:
    """
    Upload a PDF resume, extract its text, and parse it
    into structured ResumeData.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A resume PDF file is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resume files are supported.",
        )

    safe_filename = (
        f"{uuid4().hex}.pdf"
    )

    file_path = UPLOAD_DIR / safe_filename

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty.",
            )

        file_path.write_bytes(contents)

        extracted_text = extract_text_from_pdf(
            file_path
        )

        parsed_resume = parse_resume_text(
            extracted_text
        )

        return parsed_resume

    except HTTPException:
        raise

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF could not be processed.",
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal resume upload processing error.",
        ) from exc

    finally:
        if file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass