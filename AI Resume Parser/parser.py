import re
from pypdf import PdfReader


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(file_path):
    text = ""

    try:
        reader = PdfReader(file_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print("PDF reading error:", e)

    return text


# ============================================================
# BASIC INFORMATION
# ============================================================

def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    return match.group(0) if match else "Not found"


def extract_phone(text):
    patterns = [
        r"\+91[\s-]?[6-9]\d{9}",
        r"\b[6-9]\d{9}\b",
        r"\b\d{3}[\s-]\d{3}[\s-]\d{4}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group(0)

    return "Not found"


def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored_words = [
        "resume",
        "curriculum vitae",
        "cv",
        "profile",
        "about me",
        "contact",
        "objective",
        "professional summary",
        "summary",
        "career objective"
    ]

    for line in lines[:20]:

        lower_line = line.lower()

        if lower_line in ignored_words:
            continue

        if "@" in line:
            continue

        if re.search(r"\d", line):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:

            if len(line) < 40:
                return line

    return "Not found"


# ============================================================
# SKILLS DATABASE
# ============================================================

SKILLS_DATABASE = {

    "Programming": [
        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",
        "PHP",
        "Ruby",
        "Go",
        "Kotlin",
        "Swift"
    ],

    "Web Development": [
        "HTML",
        "CSS",
        "React",
        "React.js",
        "Angular",
        "Vue",
        "Node.js",
        "Node",
        "Express",
        "Express.js",
        "Bootstrap",
        "Tailwind",
        "Next.js",
        "Flask",
        "Django"
    ],

    "Database": [
        "MySQL",
        "MongoDB",
        "PostgreSQL",
        "SQLite",
        "Oracle",
        "SQL",
        "Firebase"
    ],

    "Tools": [
        "Git",
        "GitHub",
        "VS Code",
        "Docker",
        "Postman",
        "Figma",
        "Linux"
    ],

    "Data & AI": [
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "AI",
        "Data Science",
        "Pandas",
        "NumPy",
        "TensorFlow",
        "PyTorch",
        "OpenCV",
        "NLP"
    ],

    "Cloud": [
        "AWS",
        "Azure",
        "Google Cloud",
        "GCP"
    ],

    "Soft Skills": [
        "Communication",
        "Leadership",
        "Teamwork",
        "Problem Solving",
        "Time Management",
        "Adaptability"
    ]
}


def extract_skills(text):

    found_skills = {}

    text_lower = text.lower()

    for category, skills in SKILLS_DATABASE.items():

        found = []

        for skill in skills:

            if skill.lower() in text_lower:

                if skill not in found:
                    found.append(skill)

        if found:
            found_skills[category] = found

    return found_skills


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_section(text, section_names):

    lines = text.splitlines()

    start_index = None

    for i, line in enumerate(lines):

        clean = line.strip().lower()

        for section in section_names:

            if clean == section or clean.startswith(section + ":"):

                start_index = i + 1
                break

        if start_index is not None:
            break

    if start_index is None:
        return []

    result = []

    stop_words = [
        "skills",
        "technical skills",
        "education",
        "experience",
        "work experience",
        "professional experience",
        "projects",
        "certifications",
        "achievements",
        "contact",
        "about me",
        "professional summary",
        "summary",
        "languages",
        "interests",
        "references"
    ]

    for line in lines[start_index:]:

        clean = line.strip()

        if not clean:
            continue

        if clean.lower() in stop_words:
            break

        result.append(clean)

    return result


# ============================================================
# EDUCATION
# ============================================================

def extract_education(text):

    keywords = [
        "education",
        "academic background",
        "educational qualification",
        "academic qualification"
    ]

    return extract_section(text, keywords)


# ============================================================
# EXPERIENCE
# ============================================================

def extract_experience(text):

    keywords = [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship",
        "internships"
    ]

    return extract_section(text, keywords)


# ============================================================
# PROJECTS
# ============================================================

def extract_projects(text):

    keywords = [
        "projects",
        "project",
        "academic projects",
        "personal projects"
    ]

    return extract_section(text, keywords)


# ============================================================
# CERTIFICATIONS
# ============================================================

def extract_certifications(text):

    keywords = [
        "certifications",
        "certificates",
        "certification",
        "courses"
    ]

    return extract_section(text, keywords)


# ============================================================
# LINKS
# ============================================================

def extract_links(text):

    links = []

    patterns = [
        r"https?://[^\s]+",
        r"www\.[^\s]+"
    ]

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for link in matches:

            link = link.rstrip(".,);]")

            if link not in links:
                links.append(link)

    return links


# ============================================================
# LINKEDIN / GITHUB DETECTION
# ============================================================

def detect_profile_links(links):

    linkedin = []
    github = []
    portfolio = []

    for link in links:

        lower = link.lower()

        if "linkedin.com" in lower:
            linkedin.append(link)

        elif "github.com" in lower:
            github.append(link)

        else:
            portfolio.append(link)

    return {
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio
    }


# ============================================================
# KEYWORD ANALYSIS
# ============================================================

JOB_KEYWORDS = [
    "software",
    "developer",
    "web developer",
    "full stack",
    "frontend",
    "backend",
    "python",
    "java",
    "javascript",
    "react",
    "node",
    "sql",
    "database",
    "api",
    "git",
    "github",
    "machine learning",
    "artificial intelligence",
    "cloud",
    "aws",
    "project",
    "teamwork",
    "communication",
    "problem solving"
]


def analyze_keywords(text):

    text_lower = text.lower()

    found = []
    missing = []

    for keyword in JOB_KEYWORDS:

        if keyword.lower() in text_lower:

            if keyword not in found:
                found.append(keyword)

        else:

            if keyword not in missing:
                missing.append(keyword)

    return {
        "found": found,
        "missing": missing
    }


# ============================================================
# RESUME SCORE
# ============================================================

def calculate_score(
    name,
    email,
    phone,
    skills,
    education,
    experience,
    projects,
    certifications,
    links,
    text
):

    score = 0

    # Contact information - 30
    if name != "Not found":
        score += 10

    if email != "Not found":
        score += 10

    if phone != "Not found":
        score += 10

    # Skills - 20
    skill_count = sum(
        len(items)
        for items in skills.values()
    )

    if skill_count >= 8:
        score += 20

    elif skill_count >= 5:
        score += 15

    elif skill_count >= 2:
        score += 10

    elif skill_count >= 1:
        score += 5

    # Education - 10
    if education:
        score += 10

    # Experience - 10
    if experience:
        score += 10

    # Projects - 10
    if projects:
        score += 10

    # Certifications - 5
    if certifications:
        score += 5

    # Links - 5
    if links:
        score += 5

    return min(score, 100)


# ============================================================
# SCORE LEVEL
# ============================================================

def get_score_level(score):

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Very Good"

    if score >= 55:
        return "Good"

    if score >= 40:
        return "Needs Improvement"

    return "Weak"


# ============================================================
# ATS ANALYSIS
# ============================================================

def analyze_ats(
    text,
    skills,
    experience,
    education,
    projects
):

    checks = []

    text_lower = text.lower()

    # Length
    word_count = len(text.split())

    if word_count >= 300:
        checks.append({
            "title": "Resume Content",
            "status": "Good",
            "message": "Resume contains a reasonable amount of content."
        })
    else:
        checks.append({
            "title": "Resume Content",
            "status": "Improve",
            "message": "Resume appears short. Add more relevant details."
        })

    # Skills
    skill_count = sum(
        len(items)
        for items in skills.values()
    )

    if skill_count >= 5:
        checks.append({
            "title": "Technical Skills",
            "status": "Good",
            "message": "Good number of technical skills detected."
        })
    else:
        checks.append({
            "title": "Technical Skills",
            "status": "Improve",
            "message": "Add more job-relevant technical skills."
        })

    # Education
    if education:
        checks.append({
            "title": "Education",
            "status": "Good",
            "message": "Education section detected."
        })
    else:
        checks.append({
            "title": "Education",
            "status": "Improve",
            "message": "Education section was not detected."
        })

    # Experience
    if experience:
        checks.append({
            "title": "Experience",
            "status": "Good",
            "message": "Experience section detected."
        })
    else:
        checks.append({
            "title": "Experience",
            "status": "Improve",
            "message": "Add internships, training or professional experience."
        })

    # Projects
    if projects:
        checks.append({
            "title": "Projects",
            "status": "Good",
            "message": "Projects section detected."
        })
    else:
        checks.append({
            "title": "Projects",
            "status": "Improve",
            "message": "Add relevant projects to demonstrate practical skills."
        })

    # Email
    if re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    ):
        checks.append({
            "title": "Contact Information",
            "status": "Good",
            "message": "Email address detected."
        })
    else:
        checks.append({
            "title": "Contact Information",
            "status": "Improve",
            "message": "Add a professional email address."
        })

    return checks


# ============================================================
# STRENGTHS
# ============================================================

def generate_strengths(
    skills,
    education,
    experience,
    projects,
    certifications,
    links
):

    strengths = []

    skill_count = sum(
        len(items)
        for items in skills.values()
    )

    if skill_count >= 8:

        strengths.append(
            "Strong technical skill coverage"
        )

    elif skill_count >= 5:

        strengths.append(
            "Good technical skill coverage"
        )

    if education:

        strengths.append(
            "Education section is present"
        )

    if experience:

        strengths.append(
            "Professional experience is included"
        )

    if projects:

        strengths.append(
            "Projects demonstrate practical work"
        )

    if certifications:

        strengths.append(
            "Certifications add credibility"
        )

    if links:

        strengths.append(
            "Professional or portfolio links detected"
        )

    if not strengths:

        strengths.append(
            "Resume has been successfully processed"
        )

    return strengths


# ============================================================
# IMPROVEMENT SUGGESTIONS
# ============================================================

def generate_suggestions(
    name,
    email,
    phone,
    skills,
    education,
    experience,
    projects,
    certifications,
    links
):

    suggestions = []

    skill_count = sum(
        len(items)
        for items in skills.values()
    )

    if name == "Not found":

        suggestions.append(
            "Make your full name clearly visible at the top of the resume."
        )

    if email == "Not found":

        suggestions.append(
            "Add a professional email address."
        )

    if phone == "Not found":

        suggestions.append(
            "Add a phone number so recruiters can contact you."
        )

    if skill_count < 5:

        suggestions.append(
            "Add more relevant technical skills that match your target job."
        )

    if not education:

        suggestions.append(
            "Add a clear Education section."
        )

    if not experience:

        suggestions.append(
            "Add internships, work experience, or relevant training."
        )

    if not projects:

        suggestions.append(
            "Add 2–4 strong projects with technologies and achievements."
        )

    if not certifications:

        suggestions.append(
            "Consider adding relevant certifications or training."
        )

    if not links:

        suggestions.append(
            "Add LinkedIn, GitHub, or portfolio links."
        )

    if not suggestions:

        suggestions.append(
            "Your resume has a strong structure. Continue tailoring it for each job."
        )

    return suggestions


# ============================================================
# RESUME PARSER
# ============================================================

def parse_resume(file_path):

    text = extract_text_from_pdf(file_path)

    # Basic information
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    # Resume sections
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    projects = extract_projects(text)
    certifications = extract_certifications(text)
    links = extract_links(text)

    # Additional analysis
    profile_links = detect_profile_links(links)

    keyword_analysis = analyze_keywords(text)

    score = calculate_score(
        name,
        email,
        phone,
        skills,
        education,
        experience,
        projects,
        certifications,
        links,
        text
    )

    score_level = get_score_level(score)

    ats_analysis = analyze_ats(
        text,
        skills,
        experience,
        education,
        projects
    )

    strengths = generate_strengths(
        skills,
        education,
        experience,
        projects,
        certifications,
        links
    )

    suggestions = generate_suggestions(
        name,
        email,
        phone,
        skills,
        education,
        experience,
        projects,
        certifications,
        links
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "name": name,

        "email": email,

        "phone": phone,

        "skills": skills,

        "education": education,

        "experience": experience,

        "projects": projects,

        "certifications": certifications,

        "links": links,

        "profile_links": profile_links,

        "score": score,

        "score_level": score_level,

        "strengths": strengths,

        "suggestions": suggestions,

        "keyword_analysis": keyword_analysis,

        "ats_analysis": ats_analysis,

        "text": text
    }