from data.agriculture_demo import (
    farmers,
    helpers,
    problems,
    resources,
    opportunities,
)


def find_agriculture_matches(farmer_id: str):
    farmer = next(
        (farmer for farmer in farmers if farmer.id == farmer_id),
        None,
    )

    if farmer is None:
        return {
            "farmer_id": farmer_id,
            "matches": [],
            "error": "Farmer not found",
        }

    matches = []

    # ---------------------------------------------------------
    # PROBLEM MATCHING
    # ---------------------------------------------------------

    for problem in problems:
        location_match = (
            farmer.location.lower() == problem.location.lower()
        )

        farmer_skills = {
            skill.lower()
            for skill in farmer.skills
        }

        required_skills = {
            skill.lower()
            for skill in problem.required_skills
        }

        skill_overlap = farmer_skills.intersection(required_skills)

        # A problem is relevant primarily when location matches.
        # Skills can strengthen the match.
        if not location_match and not skill_overlap:
            continue

        score = 0
        reasons = []

        if location_match:
            score += 70
            reasons.append(
                f"Location match: {farmer.location}"
            )

        if skill_overlap:
            score += 30
            reasons.append(
                f"Relevant skills: {', '.join(sorted(skill_overlap))}"
            )

        matches.append({
            "type": "problem",
            "id": problem.id,
            "title": problem.title,
            "score": score,
            "reasons": reasons,
        })

    # ---------------------------------------------------------
    # HELPER MATCHING
    # ---------------------------------------------------------

    for helper in helpers:
        location_match = (
            farmer.location.lower() == helper.location.lower()
        )

        farmer_skills = {
            skill.lower()
            for skill in farmer.skills
        }

        helper_skills = {
            skill.lower()
            for skill in helper.skills
        }

        skill_overlap = farmer_skills.intersection(helper_skills)

        if not location_match and not skill_overlap:
            continue

        score = 0
        reasons = []

        if location_match:
            score += 40
            reasons.append(
                f"Location match: {farmer.location}"
            )

        if skill_overlap:
            score += 60
            reasons.append(
                f"Skill overlap: {', '.join(sorted(skill_overlap))}"
            )

        matches.append({
            "type": "helper",
            "id": helper.id,
            "title": helper.name,
            "score": score,
            "reasons": reasons,
        })

    # ---------------------------------------------------------
    # OPPORTUNITY MATCHING
    # ---------------------------------------------------------

    for opportunity in opportunities:
        location_match = (
            farmer.location.lower() == opportunity.location.lower()
        )

        farmer_interests = {
            interest.lower()
            for interest in farmer.interests
        }

        category_match = (
            opportunity.category.lower()
            in farmer_interests
        )

        if not location_match and not category_match:
            continue

        score = 0
        reasons = []

        if location_match:
            score += 50
            reasons.append(
                f"Location match: {farmer.location}"
            )

        if category_match:
            score += 50
            reasons.append(
                f"Interest match: {opportunity.category}"
            )

        matches.append({
            "type": "opportunity",
            "id": opportunity.id,
            "title": opportunity.title,
            "score": score,
            "reasons": reasons,
        })

    # Highest-confidence matches first
    matches.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return {
        "farmer_id": farmer.id,
        "farmer": farmer.name,
        "location": farmer.location,
        "matches": matches,
    }


def get_agriculture_data():
    return {
        "farmers": farmers,
        "helpers": helpers,
        "problems": problems,
        "resources": resources,
        "opportunities": opportunities,
    }