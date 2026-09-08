from .query_parser import parse_query
from .matching_engine import find_matches
from .query_enrichment import enrich_query_results
from data.demo_data import people, problems, opportunities


def target_matches_query(target, parsed):
    """
    Determine whether a problem or opportunity is relevant
    to the user's query.
    """

    # Explicit skill constraint
    if parsed["skills"]:
        target_skills = {
            skill.lower()
            for skill in target.required_skills
        }

        if not any(
            skill.lower() in target_skills
            for skill in parsed["skills"]
        ):
            return False

    # Explicit category constraint
    if parsed["categories"]:
        target_category = target.category.lower()

        if not any(
            category.lower() == target_category
            for category in parsed["categories"]
        ):
            return False

    # Explicit location constraint
    if parsed["location"]:
        if target.location.lower() != parsed["location"].lower():
            return False

    return True


def query_sang(query: str):
    parsed = parse_query(query)

    if not parsed["skills"] and not parsed["categories"] and not parsed["location"]:
        return {
            "query": query,
            "understood": parsed,
            "results": []
        }

    candidates = []

    for person in people:
        skill_overlap = len(
            set(parsed["skills"]) &
            {skill.lower() for skill in person.skills}
        )

        category_match = False

        if parsed["categories"]:
            category_match = any(
                category.lower() in {
                    interest.lower()
                    for interest in person.interests
                }
                for category in parsed["categories"]
            )

        location_match = (
            parsed["location"] is not None
            and person.location.lower() == parsed["location"].lower()
        )

        if parsed["skills"] or parsed["categories"] or parsed["location"]:
            if skill_overlap > 0 or category_match or location_match:
                candidates.append(person)

    results = []

    for person in candidates:
        matches = find_matches(person, problems, opportunities)

        for match in matches:
            if match.score <= 0:
                continue

            target = next(
                (
                    item
                    for item in problems + opportunities
                    if item.id == match.target_id
                ),
                None
            )

            if target is None:
                continue

            if not target_matches_query(target, parsed):
                continue

            results.append({
                "person": person.name,
                "match": match.model_dump()
            })

    return {
        "query": query,
        "understood": parsed,
        "results": enrich_query_results(results)
    }