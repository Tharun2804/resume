import json
from groq import Groq
from config import Config


SYSTEM_PROMPT = """You are an expert technical recruiter and resume analyst.
Analyze the resume against the job description and respond ONLY with valid JSON in this exact structure:
{
  "match_score": <integer 0-100>,
  "matched_skills": [<list of skills found in both resume and JD>],
  "missing_skills": [<list of skills required by JD but absent in resume>],
  "strengths": [<2-4 key strengths relevant to the role>],
  "gaps": [<2-4 specific gaps or concerns>],
  "recommendation": "<Shortlist | Consider | Reject>",
  "summary": "<2-3 sentence overall assessment>"
}"""


def analyze(resume_text: str, jd_text: str) -> dict:
    user_message = f"""## Job Description
{jd_text}

## Resume
{resume_text}

Analyze the resume against the job description and return the JSON response."""

    try:
        client = Groq(api_key=Config.GROQ_API_KEY)
        response = client.chat.completions.create(
            model=Config.GROQ_MODEL_ID,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1024,
        )
        content = response.choices[0].message.content.strip()

        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        return json.loads(content)

    except Exception as e:
        raise RuntimeError(f"Groq error: {str(e)}")
    except (json.JSONDecodeError, KeyError) as e:
        raise RuntimeError(f"Failed to parse AI response: {str(e)}")
