import io
import pdfplumber
from docx import Document


def extract_text(file_storage, max_chars: int) -> str:
    """Extract text from PDF or DOCX FileStorage object. Returns truncated text."""
    filename = file_storage.filename.lower()
    data = file_storage.read()

    if filename.endswith(".pdf"):
        text = _extract_pdf(data)
    elif filename.endswith(".docx"):
        text = _extract_docx(data)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are allowed.")

    text = text.strip()
    if not text:
        raise ValueError("Could not extract any text from the file. Ensure it is not scanned/image-based.")

    return text[:max_chars]


def _extract_pdf(data: bytes) -> str:
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        return "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )


def _extract_docx(data: bytes) -> str:
    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs)
