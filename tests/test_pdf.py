from pathlib import Path

import pytest
from pypdf import PdfWriter

from app.services.pdf_service import extract_text_from_pdf


def create_test_pdf(path: Path, text: str = "Test resume content.") -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with open(path, "wb") as file:
        writer.write(file)


def test_missing_pdf_raises_error(tmp_path):
    missing_file = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf(missing_file)


def test_non_pdf_file_raises_error(tmp_path):
    text_file = tmp_path / "resume.txt"
    text_file.write_text("This is not a PDF.")

    with pytest.raises(ValueError, match="Only PDF files are supported"):
        extract_text_from_pdf(text_file)


def test_pdf_without_extractable_text_raises_error(tmp_path):
    pdf_file = tmp_path / "empty.pdf"

    create_test_pdf(pdf_file)

    with pytest.raises(ValueError, match="No extractable text"):
        extract_text_from_pdf(pdf_file)