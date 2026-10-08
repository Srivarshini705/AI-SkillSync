from pathlib import Path


MAX_RESUME_SIZE = 5 * 1024 * 1024  # 5 MB
PDF_SIGNATURE = b"%PDF"


def validate_resume_file(
    filename: str | None,
    content: bytes,
) -> None:
    """
    Validate an uploaded resume before processing.

    Raises:
        ValueError: If the file is invalid or unsafe.
    """

    if not filename:
        raise ValueError("A resume PDF file is required.")

    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    if not content:
        raise ValueError("Uploaded PDF is empty.")

    if len(content) > MAX_RESUME_SIZE:
        raise ValueError(
            "Resume PDF exceeds the maximum allowed size of 5 MB."
        )

    if not content.startswith(PDF_SIGNATURE):
        raise ValueError(
            "Uploaded file is not a valid PDF."
        )