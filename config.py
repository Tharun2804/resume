import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID", "openai/gpt-oss-20b")
    MAX_FILE_BYTES = int(os.getenv("MAX_FILE_SIZE_MB", 5)) * 1024 * 1024
    ALLOWED_EXTENSIONS = {"pdf", "docx"}
    MAX_TEXT_CHARS = 12000
