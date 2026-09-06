from .models import Person, Problem, Opportunity, Match


def calculate_skill_match(person_skills, required_skills):
    if not required_skills:
        return 0.0

    person_skills_lower = {skill.lower() for skill in person_skills}
    required_skills_lower = {skill.lower() for skill in required_skills}

    matched_skills = person_skills_lower.intersection(required_skills_lower)

    return len(matched_skills) / len(required_skills_lower)

def calculate_interest_match(person_interests, target_category):
    if not target_category:
        return 0.0

    interests_lower = {interest.lower() for interest in person_interests}
    category = target_category.lower()

    if category in interests_lower:
        return 1.0

    related_concepts = {
        "sustainability": {"circular economy"},
        "agriculture": {"rural development"},
        "education": {"teaching"},
        "ai": {"machine learning"},
        "rural development": {"community outreach"},
    }

    related = related_concepts.get(category, set())

    if interests_lower.intersection(related):
        return 0.5

    return 0.0


def calculate_location_match(person_location, target_location):
    person = person_location.lower()
    target = target_location.lower()

    if person == target:
        return 1.0

    if person == "gujarat" or target == "gujarat":
        return 0.5

    return 0.0


def match_person_to_target(person, target):
    skill_match = calculate_skill_match(
        person.skills,
        target.required_skills
    )

    interest_match = calculate_interest_match(
        person.interests,
        target.category
    )

    location_match = calculate_location_match(
        person.location,
        target.location
    )

    score = (
        (skill_match * 0.60) +
        (interest_match * 0.20) +
        (location_match * 0.20)
    )

    reasons = []

    if skill_match > 0:
        matched = [
            skill for skill in target.required_skills
            if skill.lower() in {s.lower() for s in person.skills}
        ]

        reasons.append(
            f"Skill match: {', '.join(matched)} "
            f"({skill_match * 100:.0f}% of required skills)"
        )

        missing = [
            skill for skill in target.required_skills
            if skill.lower() not in {s.lower() for s in person.skills}
        ]

        if missing:
            reasons.append(
                f"Missing skills: {', '.join(missing)}"
            )

    if interest_match > 0:
        reasons.append(
            f"Interest match: {target.category}"
        )

    if location_match > 0:
        reasons.append(
            f"Location match: {person.location}"
        )

    return Match(
        target_id=target.id,
        target_type=target.__class__.__name__,
        score=round(score * 100, 2),
        reasons=reasons
    )