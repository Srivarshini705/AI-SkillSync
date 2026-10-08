import re

from app.models.resume_models import ResumeData


SECTION_ALIASES = {
    "summary": [
        "summary",
        "professional summary",
        "professional profile",
        "profile",
        "career summary",
        "objective",
        "career objective",
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "academic background and qualifications",
    ],
    "skills": [
        "technical skills",
        "skills",
        "technical expertise",
        "core skills",
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "work history",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "courses",
    ],
    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
    ],
}


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)"
)


# Important:
# These are matched as actual section headings rather than
# arbitrary occurrences of words such as "experience".
SECTION_PATTERN = re.compile(
    r"(?<![A-Za-z])("
    r"SUMMARY|"
    r"PROFESSIONAL SUMMARY|"
    r"PROFESSIONAL PROFILE|"
    r"PROFILE|"
    r"CAREER OBJECTIVE|"
    r"OBJECTIVE|"
    r"EDUCATION|"
    r"ACADEMIC BACKGROUND|"
    r"ACADEMIC QUALIFICATIONS|"
    r"EDUCATIONAL BACKGROUND|"
    r"QUALIFICATIONS|"
    r"TECHNICAL SKILLS|"
    r"SKILLS|"
    r"PROJECTS|"
    r"ACADEMIC PROJECTS|"
    r"PERSONAL PROJECTS|"
    r"EXPERIENCE|"
    r"WORK EXPERIENCE|"
    r"PROFESSIONAL EXPERIENCE|"
    r"EMPLOYMENT|"
    r"CERTIFICATIONS|"
    r"CERTIFICATES|"
    r"ACHIEVEMENTS|"
    r"ACCOMPLISHMENTS|"
    r"AWARDS|"
    r"LANGUAGES|"
    r"INTERESTS"
    r")(?![A-Za-z])",
)


def clean_text(text: str) -> str:
    """Normalize PDF-extracted text."""

    if not text:
        return ""

    text = text.replace("\r", "\n")
    text = text.replace("\t", " ")

    text = text.replace("•", "\n• ")
    text = text.replace("▪", "\n▪ ")
    text = text.replace("●", "\n● ")

    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n[ ]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def normalize_heading(text: str) -> str:
    """Normalize a section heading."""

    text = text.lower().strip()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def detect_section_heading(text: str) -> str | None:
    """Return the internal section name for a known heading."""

    normalized = normalize_heading(text)

    for section_name, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            if normalized == normalize_heading(alias):
                return section_name

    return None


def split_into_sections(text: str) -> dict[str, str]:
    """
    Split resume text using actual section headings.

    This avoids treating ordinary words such as "experience"
    inside a sentence as a section heading.
    """

    text = clean_text(text)

    matches = list(SECTION_PATTERN.finditer(text))

    sections: dict[str, str] = {}

    for index, match in enumerate(matches):
        heading = match.group(1)
        section_name = detect_section_heading(heading)

        # Languages and interests are boundaries but are not part
        # of the ResumeData model, so their content is ignored.
        if section_name is None and heading.upper() in {
            "LANGUAGES",
            "INTERESTS",
        }:
            continue

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        content = text[start:end].strip()

        if not content:
            continue

        if section_name:
            sections[section_name] = content

    return sections


def extract_email(text: str) -> str | None:
    """Extract the first email address."""

    match = EMAIL_PATTERN.search(text)

    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    """Extract the first likely phone number."""

    matches = PHONE_PATTERN.findall(text)

    for phone in matches:
        digits = re.sub(r"\D", "", phone)

        if 10 <= len(digits) <= 15:
            return phone.strip()

    return None


def extract_name(text: str) -> str | None:
    """Extract the candidate name from the resume header."""

    email_match = EMAIL_PATTERN.search(text)
    phone_match = PHONE_PATTERN.search(text)

    positions = [
        match.start()
        for match in [email_match, phone_match]
        if match
    ]

    if not positions:
        first_line = text.strip().splitlines()[0]
        return first_line.strip() if first_line else None

    prefix = text[:min(positions)]

    prefix = re.sub(
        r"(linkedin\.com/\S+|github\.com/\S+)",
        "",
        prefix,
        flags=re.IGNORECASE,
    )

    prefix = re.sub(r"[•·|]+", " ", prefix)
    prefix = re.sub(r"\s+", " ", prefix)

    name = prefix.strip(" -,:;|")

    if name and len(name.split()) <= 8:
        return name

    return None


def deduplicate_preserving_order(
    values: list[str],
) -> list[str]:
    """Remove duplicate values while preserving order."""

    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        value = value.strip()

        if not value:
            continue

        normalized = value.lower()

        if normalized not in seen:
            seen.add(normalized)
            result.append(value)

    return result


def clean_list_items(text: str) -> list[str]:
    """Convert a section into clean list items."""

    if not text:
        return []

    text = text.replace("•", "\n• ")
    text = text.replace("▪", "\n▪ ")
    text = text.replace("●", "\n● ")

    items = re.split(r"\n|•|▪|●", text)

    cleaned = []

    for item in items:
        item = re.sub(r"\s+", " ", item).strip()
        item = item.strip("-–—: ")

        if item:
            cleaned.append(item)

    return deduplicate_preserving_order(cleaned)


def parse_skills(text: str) -> list[str]:
    """
    Parse categorized technical skills.

    Example:

    Programming: Python, R
    AI/ML: Machine Learning, Generative AI
    Libraries: Pandas, NumPy
    """

    if not text:
        return []

    # Turn category labels into separators.
    text = re.sub(
        r"\b(?:Programming|AI/ML|Libraries|Web|Tools)"
        r"\s*:",
        "\n",
        text,
        flags=re.IGNORECASE,
    )

    items = re.split(r"[,;\n|]", text)

    skills = []

    for item in items:
        item = re.sub(r"\s+", " ", item).strip()

        if not item:
            continue

        if len(item) > 80:
            continue

        skills.append(item)

    return deduplicate_preserving_order(skills)

def parse_projects(text: str) -> list[str]:
    """
    Parse project entries from a projects section.

    Supports:
    - One-project-per-line resumes
    - PDF resumes with project-type markers
    - Project descriptions and bullet points
    """

    if not text:
        return []

    text = text.replace("â€¢", "•")
    text = text.replace("â–ª", "•")
    text = text.replace("â—", "•")

    lines = []

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue

        line = re.sub(
            r"^[•▪○â€¢â–ªâ—]\s*",
            "",
            line,
        )

        line = line.strip(" -–—:;")

        if line:
            lines.append(line)

    # If the section contains explicit project-type markers,
    # use them to distinguish project titles from descriptions.
    has_project_markers = any(
        re.search(
            r"\b(?:Individual\s+Project|"
            r"Team\s+Project|"
            r"Internship\s+Project)\b",
            line,
            flags=re.IGNORECASE,
        )
        for line in lines
    )

    if not has_project_markers:
        # Simple resume format: each non-empty line represents
        # a project entry.
        return deduplicate_preserving_order(lines)

    projects = []
    current_project = None

    for line in lines:
        marker_match = re.search(
            r"\b(?:Individual\s+Project|"
            r"Team\s+Project(?:\s*-\s*[^•]+)?|"
            r"Internship\s+Project)\b",
            line,
            flags=re.IGNORECASE,
        )

        if marker_match:
            title = line[:marker_match.start()].strip()

            if current_project:
                projects.append(current_project)

            current_project = title
            continue

        if current_project is None:
            current_project = line
        else:
            current_project += " " + line

    if current_project:
        projects.append(current_project)

    return deduplicate_preserving_order(projects)

def join_section(text: str) -> str | None:
    """Return a cleaned section string."""

    if not text:
        return None

    cleaned = re.sub(r"\s+", " ", text).strip()

    return cleaned if cleaned else None


def parse_resume_text(text: str) -> ResumeData:
    """
    Convert extracted resume text into structured ResumeData.
    """

    if not text or not text.strip():
        raise ValueError("Resume text cannot be empty.")

    cleaned_text = clean_text(text)

    email = extract_email(cleaned_text)
    phone = extract_phone(cleaned_text)
    name = extract_name(cleaned_text)

    sections = split_into_sections(cleaned_text)

    summary = join_section(
        sections.get("summary", "")
    )

    education = clean_list_items(
        sections.get("education", "")
    )

    skills = parse_skills(
        sections.get("skills", "")
    )

    projects = parse_projects(
        sections.get("projects", "")
    )

    experience = clean_list_items(
        sections.get("experience", "")
    )

    certifications = clean_list_items(
        sections.get("certifications", "")
    )

    achievements = clean_list_items(
        sections.get("achievements", "")
    )

    return ResumeData(
        name=name,
        email=email,
        phone=phone,
        summary=summary,
        education=education,
        skills=skills,
        projects=projects,
        experience=experience,
        certifications=certifications,
        achievements=achievements,
    )