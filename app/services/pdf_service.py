from pathlib import Path
import re

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extract readable text from a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Combined and cleaned text from all PDF pages.

    Raises:
        FileNotFoundError: If the PDF does not exist.
        ValueError: If the file is not a PDF, cannot be read,
                    contains no pages, or contains no extractable text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Provided path is not a file: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        raise ValueError(f"Unable to read PDF file: {exc}") from exc

    if not reader.pages:
        raise ValueError("PDF contains no pages.")

    extracted_pages: list[str] = []

    for page in reader.pages:
        try:
            text = page.extract_text(extraction_mode="layout") or ""
        except Exception:
            # Some PDFs contain no usable text objects or have malformed
            # content streams. Treat these as pages without extractable text.
            text = ""
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()

        if text:
            extracted_pages.append(text)

    extracted_text = "\n\n".join(extracted_pages).strip()

    if not extracted_text:
        raise ValueError(
            "No extractable text found in PDF. "
            "The PDF may be scanned or image-based."
        )

    return extracted_text