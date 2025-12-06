"""
Hybrid AI Internship Recommendation System (Console Application)

Features:
- Rule-based AI scoring to rank internships
- Offline pseudo-generative AI advice (no API key needed)
- Beginner-friendly, fully Python-based, console application
"""

from dataclasses import dataclass
from typing import List, Set


# -------------------------
# Internship Data Structure
# -------------------------

@dataclass
class Internship:
    title: str
    company: str
    skills: List[str]
    level: str       # beginner / intermediate / advanced
    domain: str      # web / ml / ai / cybersecurity / cloud / iot / general
    mode: str        # remote / onsite / hybrid


# ------------------------------------
# Knowledge Base: Internship Database
# ------------------------------------

INTERNSHIPS: List[Internship] = [
    Internship(
        title="Python Web Development Intern",
        company="TechHive Solutions",
        skills=["python", "html", "css", "django", "git"],
        level="beginner",
        domain="web",
        mode="remote",
    ),
    Internship(
        title="Frontend Web Intern",
        company="PixelCraft Studio",
        skills=["html", "css", "javascript", "react"],
        level="beginner",
        domain="web",
        mode="hybrid",
    ),
    Internship(
        title="Machine Learning Intern",
        company="DataSense Analytics",
        skills=["python", "pandas", "numpy", "ml", "scikit-learn"],
        level="intermediate",
        domain="ml",
        mode="remote",
    ),
    Internship(
        title="AI Research Assistant Intern",
        company="NeuroLabs AI",
        skills=["python", "ml", "deep learning", "pytorch"],
        level="advanced",
        domain="ai",
        mode="onsite",
    ),
    Internship(
        title="Cybersecurity Analyst Intern",
        company="SecureNet Systems",
        skills=["linux", "networking", "python", "cybersecurity"],
        level="intermediate",
        domain="cybersecurity",
        mode="onsite",
    ),
    Internship(
        title="Cloud & DevOps Intern",
        company="CloudBridge",
        skills=["linux", "docker", "aws", "git"],
        level="intermediate",
        domain="cloud",
        mode="hybrid",
    ),
    Internship(
        title="IoT & Embedded Systems Intern",
        company="SmartThings Labs",
        skills=["iot", "arduino", "sensors", "python"],
        level="beginner",
        domain="iot",
        mode="onsite",
    ),
    Internship(
        title="Data Analytics Intern",
        company="InsightPoint",
        skills=["excel", "sql", "python", "pandas"],
        level="beginner",
        domain="ml",
        mode="remote",
    ),
    Internship(
        title="Backend Developer Intern",
        company="StackFlow Technologies",
        skills=["python", "django", "rest api", "databases"],
        level="intermediate",
        domain="web",
        mode="remote",
    ),
    Internship(
        title="General Tech Intern",
        company="BrightStart Innovations",
        skills=["communication", "teamwork", "python"],
        level="beginner",
        domain="general",
        mode="hybrid",
    ),
]


# ------------------------------
# Helper Functions
# ------------------------------

def normalize_list(items: List[str]) -> List[str]:
    return [item.strip().lower() for item in items if item.strip()]


def get_user_input():
    print("=== Internship Recommendation Assistant ===\n")

    raw_skills = input("Enter your skills (comma-separated, e.g. python, html, css, iot):\n> ")
    user_skills = set(normalize_list(raw_skills.split(",")))

    level = input("\nEnter your experience level (beginner / intermediate / advanced):\n> ").strip().lower()

    domain_pref = input("\nPreferred domain (web / ml / ai / cybersecurity / cloud / iot / any):\n> ").strip().lower()

    mode_pref = input("\nPreferred work mode (remote / onsite / hybrid / any):\n> ").strip().lower()

    print("\nThanks! Calculating best matches...\n")

    return user_skills, level, domain_pref, mode_pref


# ------------------------------
# Rule-Based AI Scoring System
# ------------------------------

def score_internship(internship: Internship, user_skills: Set[str], level: str, domain_pref: str, mode_pref: str) -> int:
    matched_skills = set(internship.skills) & user_skills
    skill_score = len(matched_skills) * 2

    domain_score = 2 if (domain_pref != "any" and domain_pref == internship.domain) else 0
    mode_score = 1 if (mode_pref != "any" and mode_pref == internship.mode) else 0

    level_score = 0
    if level == internship.level:
        level_score = 1
    elif level == "beginner" and internship.level == "intermediate":
        level_score = 1

    return skill_score + domain_score + mode_score + level_score


def recommend_internships(user_skills, level, domain_pref, mode_pref):
    scored = []
    for internship in INTERNSHIPS:
        score = score_internship(internship, user_skills, level, domain_pref, mode_pref)
        if score > 0:
            scored.append((score, internship))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored


# -------------------------------------------------------
# Offline “Pseudo-Generative AI” — No API Needed
# -------------------------------------------------------

def generate_ai_advice(user_skills, level, domain_pref, matches):
    advice = []

    skills_str = ", ".join(user_skills) if user_skills else "no listed skills"

    advice.append(f"\nBased on your skills ({skills_str}) and your preferred domain ({domain_pref.upper()}):\n")

    # Domain-based advice
    domain_map = {
        "web": "Try building small frontend or Django projects. Learn APIs.",
        "ml": "Focus on numpy, pandas, and ML basics. Try Kaggle.",
        "ai": "Explore neural networks. Learn PyTorch or TensorFlow.",
        "cybersecurity": "Strengthen Linux and networking. Try simple CTFs.",
        "cloud": "Practice AWS basics and containerization (Docker).",
        "iot": "Build Arduino/Raspberry Pi projects. Learn MQTT & sensors.",
    }

    if domain_pref in domain_map:
        advice.append("- " + domain_map[domain_pref])
    else:
        advice.append("- Explore multiple domains to discover your interest.")

    # Skill-based suggestions
    if "python" in user_skills:
        advice.append("- Python opens paths in Web, ML, AI, Cybersecurity, and IoT.")
    if "html" in user_skills or "css" in user_skills:
        advice.append("- Your web skills suggest trying frontend or full-stack roles.")
    if "iot" in user_skills:
        advice.append("- IoT skill detected — consider embedded systems internships.")

    # Experience level
    if level == "beginner":
        advice.append("- Start with beginner-friendly startups and build 1–2 mini projects.")
    elif level == "intermediate":
        advice.append("- You can target more technical roles requiring prior experience.")
    else:
        advice.append("- Advanced level unlocks research roles in AI and systems.")

    # Top match highlight
    if matches:
        top = matches[0][1].title
        advice.append(f"- Your strongest match is: '{top}'.")
    else:
        advice.append("- No strong match found; try upskilling in Python or Web Dev.")

    advice.append("\nOverall, keep building projects and applying consistently!")

    return "\n".join(advice)


# ------------------------------
# MAIN PROGRAM
# ------------------------------

def main():
    user_skills, level, domain_pref, mode_pref = get_user_input()

    matches = recommend_internships(user_skills, level, domain_pref, mode_pref)

    if not matches:
        print("No strong matches found.\nTry adding skills like python, html, sql.")
        return

    print("Top Internship Recommendations:\n")
    for rank, (score, internship) in enumerate(matches[:5], start=1):
        print(f"{rank}. {internship.title} at {internship.company}")
        print(f"   Domain: {internship.domain.upper()} | Level: {internship.level} | Mode: {internship.mode}")
        print(f"   Score: {score}")
        print()

    # ------------------------------
    # OPTIONAL: AI-Enhanced Advice
    # ------------------------------
    use_ai = input("Would you like AI-enhanced guidance? (yes/no): ").strip().lower()

    if use_ai == "yes":
        print("\nAI-Generated Personalized Advice:\n")
        print(generate_ai_advice(user_skills, level, domain_pref, matches))


if __name__ == "__main__":
    main()
