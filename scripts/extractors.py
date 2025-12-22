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
