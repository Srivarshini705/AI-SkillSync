RESUME_GENERATION_SYSTEM_PROMPT = """
You are a professional resume writing assistant.

Your task is to improve and structure resume content provided by a
candidate.

IMPORTANT RULES:

1. Never invent candidate information.
2. Never create a degree that the candidate did not provide.
3. Never create a company, job position, or work experience.
4. Never create certifications that were not provided.
5. Never create skills that were not provided.
6. Never create projects that were not provided.
7. Never create achievements that were not provided.
8. You may improve grammar, clarity, professionalism, and wording.
9. You may rewrite existing experience and project descriptions
   into stronger professional statements.
10. Keep the meaning of the candidate's original information.
11. Do not exaggerate responsibilities or achievements.
12. Return only valid JSON.
"""


def build_resume_generation_prompt(
    name: str | None,
    email: str | None,
    phone: str | None,
    summary: str | None,
    education: list[str],
    skills: list[str],
    projects: list[str],
    experience: list[str],
    certifications: list[str],
    achievements: list[str],
) -> str:
    """
    Build the user prompt for AI-assisted resume generation.
    """

    return f"""
Create professionally written resume content from the candidate
information below.

CANDIDATE INFORMATION
---------------------

Name:
{name or "Not provided"}

Email:
{email or "Not provided"}

Phone:
{phone or "Not provided"}

Summary:
{summary or "Not provided"}

Education:
{education or ["Not provided"]}

Skills:
{skills or ["Not provided"]}

Projects:
{projects or ["Not provided"]}

Experience:
{experience or ["Not provided"]}

Certifications:
{certifications or ["Not provided"]}

Achievements:
{achievements or ["Not provided"]}

---------------------

Improve the wording while preserving the candidate's actual
information.

Return JSON with exactly these fields:

{{
    "name": "",
    "email": "",
    "phone": "",
    "summary": "",
    "education": [],
    "skills": [],
    "projects": [],
    "experience": [],
    "certifications": [],
    "achievements": []
}}

Rules:

- Keep all factual information supplied by the candidate.
- Improve the professional wording of summary, projects,
  experience, and achievements when appropriate.
- Do not add fictional information.
- Do not add skills simply because they are common for the candidate's
  field.
- Do not add companies, positions, degrees, certifications, projects,
  achievements, dates, or technologies that were not provided.
- If a field is not provided, return an empty string or empty list.
- Return JSON only.
"""