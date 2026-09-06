from .models import Person, Problem, Opportunity, Match


def calculate_skill_match(person_skills, required_skills):
    if not required_skills:
        return 0.0

    person_skills_lower = {skill.lower() for skill in person_skills}
    required_skills_lower = {skill.lower() for skill in required_skills}

    matched_skills = person_skills_lower.intersection(required_skills_lower)

    return len(matched_skills) / len(required_skills_lower)


def calculate_location_match(person_location, target_location):
    return 1.0 if person_location.lower() == target_location.lower() else 0.0


def match_person_to_target(person, target):
    skill_match = calculate_skill_match(
        person.skills,
        target.required_skills
    )

    location_match = calculate_location_match(
        person.location,
        target.location
    )

    score = (skill_match * 0.70) + (location_match * 0.30)

    reasons = []

    if skill_match > 0:
        matched = [
            skill for skill in target.required_skills
            if skill.lower() in {s.lower() for s in person.skills}
        ]
        reasons.append(
            f"Skill match: {', '.join(matched)}"
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
