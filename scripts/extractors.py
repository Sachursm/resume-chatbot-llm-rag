# Rule-Based Resume Fields
import re

def extract_name(text: str):
    for line in text.split("\n"):
        if line.isupper() and len(line.split()) >= 2:
            return line.strip()
    return None


def extract_email(text: str):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group() if match else None


def extract_phone(text: str):
    match = re.search(r"\b\d{10}\b", text)
    return match.group() if match else None


def extract_skills(text: str):
    lines = text.split("\n")
    skills = []
    capture = False

    for line in lines:
        line = line.strip()

        if line.upper() == "SKILLS":
            capture = True
            continue

        if capture:
            if line.isupper() and len(line) < 25:
                break
            if line:
                skills.append(line)

    return skills

import re

def extract_company(resume_text):
    text = resume_text

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # Extract Professional Experience block
    match = re.search(
        r'(PROFESSIONAL EXPERIENCE.*?SKILLS|PROFESSIONAL EXPERIENCE.*?$)',
        text,
        re.IGNORECASE
    )

    if not match:
        return "Company not found"

    exp_section = match.group(1)

    # Debug (optional)
    # print("\n---- EXPERIENCE SECTION ----\n", exp_section[:400])

    # Common pattern → Job Title\nCOMPANY NAME
    company_regex_patterns = [
        r'\b([A-Z][A-Z\s&]+TECHNOLOGIES)\b',      # CYSONET TECHNOLOGIES like uppercase companies
        r'\b([A-Z][A-Z\s&]+PVT LTD)\b',
        r'\b([A-Z][A-Z\s&]+LIMITED)\b',
        r'[A-Z][A-Za-z\s&]+ Technologies',
        r'[A-Z][A-Za-z\s&]+ Pvt Ltd',
        r'[A-Z][A-Za-z\s&]+ Limited',
    ]

    for pattern in company_regex_patterns:
        company = re.search(pattern, exp_section)
        if company:
            return company.group(1).strip()

    # Fallback: first uppercase line
    fallback = re.search(r'\b([A-Z][A-Z\s]{3,})\b', exp_section)
    if fallback:
        return fallback.group(1).strip()

    return "Company not found"
