# =========================================================
# SkillSync AI - Skill Gap Analysis
# =========================================================


# =========================================================
# MASTER SKILL LIST
# =========================================================

ALL_SKILLS = sorted([
    "API Development",
    "AWS",
    "Authentication",
    "Authorization",
    "C",
    "C#",
    "C++",
    "CI/CD",
    "Cloud Computing",
    "Computer Networks",
    "Computer Vision",
    "CSS",
    "Dart",
    "Data Analysis",
    "Data Structures & Algorithms",
    "Data Visualization",
    "Debugging",
    "Deep Learning",
    "Docker",
    "DOM",
    "Elixir",
    "Excel",
    "F#",
    "Generative AI",
    "Git",
    "GitHub",
    "Go",
    "Google Cloud",
    "GraphQL",
    "Haskell",
    "HTML",
    "HTTP",
    "HTTPS",
    "Java",
    "JavaScript",
    "Jupyter Notebook",
    "JSON",
    "Kotlin",
    "Large Language Models",
    "Linux",
    "Lua",
    "Machine Learning",
    "MATLAB",
    "Microsoft Azure",
    "Microservices",
    "MongoDB",
    "MySQL",
    "Natural Language Processing",
    "NumPy",
    "OOP",
    "Operating Systems",
    "Objective-C",
    "Oracle",
    "Pandas",
    "Perl",
    "PHP",
    "PostgreSQL",
    "Postman",
    "Power BI",
    "Prompt Engineering",
    "Python",
    "R",
    "RAG",
    "REST APIs",
    "Redis",
    "Ruby",
    "Rust",
    "Scala",
    "Security",
    "Software Testing",
    "SQL",
    "SQLite",
    "Statistics",
    "Swift",
    "Tableau",
    "TypeScript",
    "VS Code",
    "Web APIs",
    "WebSockets",
    "XML"
])


# =========================================================
# CAREER SKILLS
# =========================================================

CAREER_SKILLS = {

    "AI Engineer": [
        "Python",
        "Data Structures & Algorithms",
        "NumPy",
        "Pandas",
        "Statistics",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "Computer Vision",
        "Generative AI",
        "Large Language Models",
        "RAG",
        "API Development",
        "Git",
        "Docker",
        "Cloud Computing"
    ],

    "AI/ML Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Statistics",
        "Data Structures & Algorithms",
        "Machine Learning",
        "Deep Learning",
        "Git",
        "Docker",
        "Cloud Computing"
    ],

    "Backend Developer": [
        "SQL",
        "REST APIs",
        "API Development",
        "HTTP",
        "JSON",
        "Authentication",
        "Authorization",
        "Git",
        "GitHub",
        "Software Testing",
        "Debugging",
        "Docker"
    ],

    "Business Intelligence Analyst": [
        "SQL",
        "Excel",
        "Data Analysis",
        "Statistics",
        "Data Visualization",
        "Power BI",
        "Tableau"
    ],

    "Cloud Engineer": [
        "Cloud Computing",
        "Linux",
        "Computer Networks",
        "Operating Systems",
        "Docker",
        "Git",
        "CI/CD"
    ],

    "Cybersecurity Analyst": [
        "Computer Networks",
        "Operating Systems",
        "Linux",
        "HTTP",
        "HTTPS",
        "Authentication",
        "Authorization",
        "Security",
        "Software Testing",
        "Debugging",
        "Git"
    ],

    "Data Analyst": [
        "SQL",
        "Excel",
        "Data Analysis",
        "Statistics",
        "Data Visualization",
        "Power BI",
        "Tableau",
        "Pandas",
        "Python"
    ],

    "Data Engineer": [
        "Python",
        "SQL",
        "PostgreSQL",
        "MySQL",
        "Data Structures & Algorithms",
        "Git",
        "Docker",
        "Cloud Computing"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Statistics",
        "Data Analysis",
        "Data Visualization",
        "Machine Learning",
        "Git",
        "Jupyter Notebook"
    ],

    "Database Developer": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "SQLite",
        "Redis",
        "Git",
        "Debugging"
    ],

    "DevOps Engineer": [
        "Linux",
        "Git",
        "GitHub",
        "CI/CD",
        "Docker",
        "Cloud Computing",
        "Software Testing",
        "Debugging"
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "DOM",
        "Web APIs",
        "REST APIs",
        "Git",
        "GitHub",
        "Software Testing",
        "Debugging"
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "TypeScript",
        "DOM",
        "Web APIs",
        "REST APIs",
        "SQL",
        "Git",
        "GitHub",
        "Authentication",
        "Authorization",
        "Software Testing",
        "Docker"
    ],

    "Java Developer": [
        "Java",
        "OOP",
        "Data Structures & Algorithms",
        "SQL",
        "REST APIs",
        "API Development",
        "Git",
        "GitHub",
        "Software Testing",
        "Debugging"
    ],

    "Machine Learning Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Statistics",
        "Data Structures & Algorithms",
        "Machine Learning",
        "Deep Learning",
        "Git",
        "Docker",
        "Cloud Computing",
        "API Development"
    ],

    "Python Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Pandas",
        "NumPy",
        "Data Analysis",
        "Statistics",
        "Data Visualization",
        "Power BI"
    ],

    "Python Developer": [
        "Python",
        "OOP",
        "Data Structures & Algorithms",
        "SQL",
        "REST APIs",
        "API Development",
        "Git",
        "GitHub",
        "Software Testing",
        "Debugging"
    ],

    "QA / Test Engineer": [
        "Software Testing",
        "Debugging",
        "SQL",
        "REST APIs",
        "API Development",
        "Git",
        "GitHub",
        "Postman"
    ],

    "Software Developer": [
        "Data Structures & Algorithms",
        "OOP",
        "SQL",
        "Git",
        "GitHub",
        "Software Testing",
        "Debugging",
        "Operating Systems"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "DOM",
        "Web APIs",
        "REST APIs",
        "HTTP",
        "JSON",
        "Git",
        "GitHub"
    ]
}


# =========================================================
# ALTERNATIVE SKILLS
# =========================================================

ROLE_ALTERNATIVES = {

    "Software Developer": [
        ["Python", "Java", "C++", "C#"]
    ],

    "Backend Developer": [
        ["Python", "Java", "JavaScript", "Go", "C#", "PHP"]
    ],

    "Full Stack Developer": [
        ["JavaScript", "TypeScript"],
        ["Python", "Java", "JavaScript", "C#", "PHP"]
    ],

    "Web Developer": [
        ["JavaScript", "TypeScript"]
    ],

    "Data Analyst": [
        ["Python", "R"]
    ],

    "Data Engineer": [
        ["Python", "Java", "Scala"]
    ],

    "QA / Test Engineer": [
        ["Python", "Java", "JavaScript", "C#"]
    ],

    "DevOps Engineer": [
        ["Python", "Go", "JavaScript"]
    ]
}


# =========================================================
# GET SKILL GAP
# =========================================================

def get_skill_gap(student_skills, target_role):

    required_skills = CAREER_SKILLS.get(
        target_role,
        []
    )

    student_skill_names = {
        skill.strip().lower()
        for skill in student_skills
    }

    missing_skills = []

    # Normal required skills
    for skill in required_skills:

        if skill.lower() not in student_skill_names:
            missing_skills.append(skill)

    # Alternative skills
    alternatives = ROLE_ALTERNATIVES.get(
        target_role,
        []
    )

    for group in alternatives:

        has_one = any(
            skill.lower() in student_skill_names
            for skill in group
        )

        if not has_one:

            missing_skills.append(
                "One of: " + " / ".join(group)
            )

    return required_skills, missing_skills


# =========================================================
# GENERATE ROADMAP
# =========================================================

def generate_roadmap(missing_skills):

    roadmap = []

    for index, skill in enumerate(
        missing_skills,
        start=1
    ):

        roadmap.append(
            f"{index}. Learn {skill}"
        )

    return roadmap


# =========================================================
# CALCULATE SKILL MATCH
# =========================================================

def calculate_skill_match(
    student_skills,
    target_role
):

    required_skills = CAREER_SKILLS.get(
        target_role,
        []
    )

    alternatives = ROLE_ALTERNATIVES.get(
        target_role,
        []
    )

    student_skill_names = {
        skill.strip().lower()
        for skill in student_skills
    }

    matched_count = 0

    for skill in required_skills:

        if skill.lower() in student_skill_names:
            matched_count += 1

    alternative_count = 0

    for group in alternatives:

        if any(
            skill.lower() in student_skill_names
            for skill in group
        ):

            alternative_count += 1

    total_requirements = (
        len(required_skills)
        + len(alternatives)
    )

    total_matched = (
        matched_count
        + alternative_count
    )

    if total_requirements == 0:
        return 0

    return round(
        (total_matched / total_requirements) * 100
    )


# =========================================================
# GET MATCHED SKILLS
# =========================================================

def get_matched_skills(
    student_skills,
    target_role
):

    required_skills = CAREER_SKILLS.get(
        target_role,
        []
    )

    student_skill_names = {
        skill.strip().lower()
        for skill in student_skills
    }

    matched_skills = []

    for skill in required_skills:

        if skill.lower() in student_skill_names:
            matched_skills.append(skill)

    return matched_skills