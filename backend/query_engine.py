from .query_parser import parse_query
from .matching_engine import find_matches
from data.demo_data import people, problems, opportunities


def query_sang(query: str):
    parsed = parse_query(query)

    candidates = []

    for person in people:
        skill_overlap = len(
            set(parsed["skills"]) &
            {skill.lower() for skill in person.skills}
        )

        location_match = (
            parsed["location"] is None
            or person.location.lower() == parsed["location"].lower()
        )

        if skill_overlap > 0 or location_match:
            candidates.append(person)

    results = []

    for person in candidates:
        matches = find_matches(person, problems, opportunities)

        for match in matches:
            if match.score > 0:
                results.append({
                    "person": person.name,
                    "match": match.model_dump()
                })

    return {
        "query": query,
        "understood": parsed,
        "results": results
    }
