import re

# ---------- Settings (lists we search for) ----------

SKILLS_LIST = [
    "python", "r", "java", "c++", "c", "javascript", "sql", "html", "css",
    "numpy", "pandas", "matplotlib", "seaborn", "scikit-learn", "tensorflow",
    "pytorch", "streamlit", "flask", "django", "dplyr", "ggplot2",
    "machine learning", "deep learning", "data visualization",
    "exploratory data analysis", "statistics", "linear algebra",
    "git", "github", "jupyter notebook", "vs code", "excel", "power bi",
    "tableau", "mysql", "mongodb", "docker", "aws",
]

SECTION_ALIASES = {
    "education": ["education", "academics", "academic background"],
    "skills": ["skills", "technical skills", "key skills"],
    "projects": ["projects", "academic projects", "personal projects"],
    "experience": ["experience", "work experience", "internship", "internships"],
    "certifications": ["certifications", "certificates"],
    "summary": ["summary", "profile summary", "objective", "profile"],
    "achievements": ["achievements", "awards"],
}

IMPORTANT_KEYWORDS = ["github", "linkedin", "python", "project"]


def skill_in_text(skill, text):
    pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None


def detect_skills(resume_text):
    text = resume_text.lower()
    found_skills = []

    for skill in SKILLS_LIST:
        if skill_in_text(skill, text):
            found_skills.append(skill)

    return found_skills



def detect_sections(resume_text):
    lines = resume_text.split("\n")
    found_sections = []

    for line in lines:
        clean_line = line.strip().lower()

        for section_name, aliases in SECTION_ALIASES.items():
            if clean_line in aliases and section_name not in found_sections:
                found_sections.append(section_name)

    return found_sections




def check_keywords(resume_text):
    text = resume_text.lower()
    present = []
    missing = []

    for keyword in IMPORTANT_KEYWORDS:
        if keyword in text:
            present.append(keyword)
        else:
            missing.append(keyword)

    has_email = "@" in resume_text

    return present, missing, has_email
# ---------- Scoring ----------

SECTION_POINTS = {
    "education": 8,
    "skills": 8,
    "projects": 8,
    "experience": 10,
    "summary": 6,
}


def score_sections(found_sections):
    points = 0

    for section_name, section_points in SECTION_POINTS.items():
        if section_name in found_sections:
            points += section_points

    return points


def score_skills(found_skills):
    points = len(found_skills) * 3

    if points > 30:
        points = 30

    return points


def score_contact(resume_text):
    text = resume_text.lower()
    points = 0

    if "@" in resume_text:
        points += 8
    if "github" in text:
        points += 6
    if "linkedin" in text:
        points += 6

    return points


def score_length(resume_text):
    word_count = len(resume_text.split())

    if 250 <= word_count <= 900:
        return 10
    elif 150 <= word_count < 250 or 900 < word_count <= 1200:
        return 5
    else:
        return 0


def calculate_score(resume_text):
    skills = detect_skills(resume_text)
    sections = detect_sections(resume_text)

    breakdown = {
        "Sections": score_sections(sections),
        "Skills": score_skills(skills),
        "Contact & links": score_contact(resume_text),
        "Length": score_length(resume_text),
    }

    total = sum(breakdown.values())
    return total, breakdown