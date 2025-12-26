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

def extract_company(text):
    text_lower = text.lower()

    # Common headings seen in resumes
    patterns = [
        r"company[:\-]\s*(.*)",
        r"organisation[:\-]\s*(.*)",
        r"organization[:\-]\s*(.*)",
        r"work experience[:\-]\s*((.|\n)*?)\n\n",
        r"experience[:\-]\s*((.|\n)*?)\n\n"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result = match.group(1).strip()
            if len(result) > 3:
                return result

    # fallback if company appears in bullet list section
    lines = text.split("\n")
    for line in lines:
        if "company" in line.lower() or "experience" in line.lower():
            return line.strip()

    return "Company / Experience information not found"
