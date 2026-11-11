import re


ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_JD_CHARS = 8000


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file(file_storage, max_bytes: int):
    """Raises ValueError on invalid file."""
    if not file_storage or file_storage.filename == "":
        raise ValueError("No file provided.")
    if not allowed_file(file_storage.filename):
        raise ValueError("Only PDF and DOCX files are accepted.")
    # Check size by reading into memory (stream)
    file_storage.seek(0, 2)
    size = file_storage.tell()
    file_storage.seek(0)
    if size > max_bytes:
        raise ValueError(f"File exceeds maximum allowed size of {max_bytes // (1024*1024)} MB.")


def sanitize_jd(text: str) -> str:
    """Strip HTML tags and limit JD text length."""
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()[:MAX_JD_CHARS]
