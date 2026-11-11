# Resume Analyzer

AI-powered resume screener using AWS Bedrock (Claude 3 Haiku).

## Setup

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Configure environment
Copy `.env.example` to `.env` and fill in your values:
```
copy .env.example .env
```

Required values in `.env`:
- `AWS_REGION` — your AWS region (e.g. `us-east-1`)
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` — IAM credentials with `bedrock:InvokeModel` permission
- `SECRET_KEY` — any random string for Flask sessions

### 3. Enable Bedrock model access
In AWS Console → Bedrock → Model Access → enable **Claude 3 Haiku**.

### 4. Run
```
python app.py
```
Visit: http://localhost:5000

## Architecture

```
app.py              # Routes + error handling + rate limiting
config.py           # All config from environment variables
services/
  parser.py         # PDF/DOCX text extraction (in-memory, no disk writes)
  validator.py      # File type, size, and input sanitization
  analyzer.py       # AWS Bedrock API call + response parsing
templates/
  base.html         # Layout with Bootstrap 5
  index.html        # Upload form
  result.html       # Structured results display
```

## Security Notes
- Files are processed in-memory only — never written to disk
- File type validated by extension + content
- JD input sanitized (HTML stripped, length capped)
- Rate limited: 10 analyses per IP per hour
- All config via environment variables (no hardcoded secrets)
- Max file size: 5 MB (configurable via `MAX_FILE_SIZE_MB`)

## Context Window Management
- Resume text capped at 12,000 characters (~3,000 tokens)
- JD text capped at 8,000 characters (~2,000 tokens)
- AI response capped at 1,024 tokens
- Total prompt stays well within Claude 3 Haiku's 200K token limit while keeping latency low
