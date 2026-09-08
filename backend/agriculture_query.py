import re

from data.agriculture_demo import (
    problems,
    helpers,
    resources,
    opportunities,
)


KNOWN_LOCATIONS = [
    "rajkot",
    "ahmedabad",
    "surat",
]

PROBLEM_KEYWORDS = {
    "pest": "Crop Pest Infestation",
    "insect": "Crop Pest Infestation",
    "insects": "Crop Pest Infestation",
    "pest infestation": "Crop Pest Infestation",

    "irrigation": "Irrigation Challenge",
    "water": "Irrigation Challenge",
    "watering": "Irrigation Challenge",

    "soil": "Soil Health Problem",
    "soil health": "Soil Health Problem",
}


def parse_agriculture_query(query: str):
    query_lower = query.lower()

    location = None
    location_mentioned = False

    # First detect supported locations.
    for city in KNOWN_LOCATIONS:
        if re.search(r"\b" + re.escape(city) + r"\b", query_lower):
            location = city.title()
            location_mentioned = True
            break

    # If no supported location was found, detect whether
    # the user explicitly mentioned another location.
    if not location_mentioned:
        location_patterns = [
            r"\bin ([A-Za-z]+)\b",
            r"\bfrom ([A-Za-z]+)\b",
            r"\bat ([A-Za-z]+)\b",
            r"\bnear ([A-Za-z]+)\b",
        ]

        for pattern in location_patterns:
            match = re.search(pattern, query_lower)

            if match:
                location = match.group(1).title()
                location_mentioned = True
                break

    problem_title = None

    for keyword, title in sorted(
        PROBLEM_KEYWORDS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if re.search(r"\b" + re.escape(keyword) + r"\b", query_lower):
            problem_title = title
            break

    return {
        "original_query": query,
        "location": location,
        "location_mentioned": location_mentioned,
        "problem": problem_title,
    }


def query_agriculture(query: str):
    parsed = parse_agriculture_query(query)

    # We need to understand an actual supported agricultural problem.
    if not parsed["problem"]:
        return {
            "query": query,
            "understood": parsed,
            "results": [],
        }

    # If the user explicitly mentioned a location that is not
    # supported by the current prototype, reject the query.
    supported_locations = [
        city.title()
        for city in KNOWN_LOCATIONS
    ]

    if (
        parsed["location_mentioned"]
        and parsed["location"] not in supported_locations
    ):
        return {
            "query": query,
            "understood": parsed,
            "results": [],
        }

    matching_problems = []

    for problem in problems:
        location_match = (
            not parsed["location_mentioned"]
            or problem.location.lower()
            == parsed["location"].lower()
        )

        problem_match = (
            problem.title == parsed["problem"]
        )

        if location_match and problem_match:
            matching_problems.append(problem)

    results = []

    for problem in matching_problems:

        helper_matches = []

        for helper in helpers:
            helper_skills = {
                skill.lower()
                for skill in helper.skills
            }

            required_skills = {
                skill.lower()
                for skill in problem.required_skills
            }

            expertise_match = bool(
                helper_skills.intersection(required_skills)
            )

            location_match = (
                helper.location.lower()
                == problem.location.lower()
            )

            if expertise_match and location_match:
                helper_matches.append({
                    "id": helper.id,
                    "name": helper.name,
                    "location": helper.location,
                    "skills": helper.skills,
                    "reason": (
                        "Relevant expertise and same-location match."
                    ),
                })

        resource_matches = [
            {
                "id": resource.id,
                "name": resource.name,
                "type": resource.resource_type,
                "reason": (
                    "Resource matches the problem location."
                ),
            }
            for resource in resources
            if resource.location.lower()
            == problem.location.lower()
        ]

        opportunity_matches = [
            {
                "id": opportunity.id,
                "title": opportunity.title,
                "organization": opportunity.organization,
                "reason": (
                    "Opportunity matches the agricultural problem context "
                    "and location."
                ),
            }
            for opportunity in opportunities
            if opportunity.location.lower()
            == problem.location.lower()
        ]

        results.append({
            "problem": {
                "id": problem.id,
                "title": problem.title,
                "description": problem.description,
                "location": problem.location,
            },
            "helpers": helper_matches,
            "resources": resource_matches,
            "opportunities": opportunity_matches,
        })

    return {
        "query": query,
        "understood": parsed,
        "results": results,
    }