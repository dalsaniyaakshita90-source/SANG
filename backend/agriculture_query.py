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
    "pest control": "Crop Pest Infestation",

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

    # ---------------------------------------------------------
    # DETECT SUPPORTED LOCATIONS
    # ---------------------------------------------------------

    for city in KNOWN_LOCATIONS:
        if re.search(
            r"\b" + re.escape(city) + r"\b",
            query_lower,
        ):
            location = city.title()
            location_mentioned = True
            break

    # ---------------------------------------------------------
    # DETECT EXPLICITLY MENTIONED OTHER LOCATIONS
    # ---------------------------------------------------------

    if not location_mentioned:

        location_patterns = [
            r"\bin ([A-Za-z]+)\b",
            r"\bfrom ([A-Za-z]+)\b",
            r"\bat ([A-Za-z]+)\b",
            r"\bnear ([A-Za-z]+)\b",
        ]

        for pattern in location_patterns:

            match = re.search(
                pattern,
                query_lower,
            )

            if match:

                location = match.group(1).title()
                location_mentioned = True

                break

    # ---------------------------------------------------------
    # DETECT AGRICULTURAL PROBLEM
    # ---------------------------------------------------------

    problem_title = None

    for keyword, title in sorted(
        PROBLEM_KEYWORDS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):

        if re.search(
            r"\b" + re.escape(keyword) + r"\b",
            query_lower,
        ):

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

    # ---------------------------------------------------------
    # NO AGRICULTURAL PROBLEM UNDERSTOOD
    # ---------------------------------------------------------

    if not parsed["problem"]:

        return {
            "query": query,
            "understood": parsed,
            "results": [],
        }

    # ---------------------------------------------------------
    # LOCATION REQUIRED
    # ---------------------------------------------------------

    if not parsed["location_mentioned"]:

        return {
            "query": query,
            "understood": parsed,
            "results": [],
            "needs_location": True,
            "prompt": (
                "I understand the agricultural problem. "
                "What city or village are you in?"
            ),
        }

    # ---------------------------------------------------------
    # REJECT UNSUPPORTED LOCATION
    # ---------------------------------------------------------

    supported_locations = [
        city.title()
        for city in KNOWN_LOCATIONS
    ]

    if parsed["location"] not in supported_locations:

        return {
            "query": query,
            "understood": parsed,
            "results": [],
            "unsupported_location": True,
            "prompt": (
                "I currently need a supported prototype location "
                "to find a verified local match."
            ),
        }

    # ---------------------------------------------------------
    # FIND EXACT PROBLEM + LOCATION
    # ---------------------------------------------------------

    matching_problems = []

    for problem in problems:

        location_match = (
            problem.location.lower()
            == parsed["location"].lower()
        )

        problem_match = (
            problem.title
            == parsed["problem"]
        )

        if location_match and problem_match:

            matching_problems.append(problem)

    # ---------------------------------------------------------
    # BUILD MATCH RESULTS
    # ---------------------------------------------------------

    results = []

    for problem in matching_problems:

        # -----------------------------------------------------
        # HELPER MATCHING
        # -----------------------------------------------------

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

            expertise_overlap = (
                helper_skills.intersection(
                    required_skills
                )
            )

            expertise_match = bool(
                expertise_overlap
            )

            location_match = (
                helper.location.lower()
                == problem.location.lower()
            )

            if expertise_match and location_match:

                reasons = [
                    f"Same location: {problem.location}",
                    (
                        "Relevant expertise: "
                        + ", ".join(
                            sorted(expertise_overlap)
                        )
                    ),
                    (
                        "Directly related to "
                        f"{problem.title.lower()}."
                    ),
                ]

                helper_matches.append({

                    "id": helper.id,

                    "name": helper.name,

                    "location": helper.location,

                    "skills": helper.skills,

                    "reason": (
                        "Same location + relevant expertise "
                        "+ direct problem relevance."
                    ),

                    "reasons": reasons,

                })

        # -----------------------------------------------------
        # RESOURCE MATCHING
        # -----------------------------------------------------

        resource_matches = []

        for resource in resources:

            location_match = (
                resource.location.lower()
                == problem.location.lower()
            )

            if not location_match:
                continue

            reasons = [
                f"Available in {problem.location}",
                (
                    "Relevant to "
                    f"{problem.title.lower()}."
                ),
            ]

            resource_matches.append({

                "id": resource.id,

                "name": resource.name,

                "type": resource.resource_type,

                "reason": (
                    "Location match + direct problem relevance."
                ),

                "reasons": reasons,

            })

        # -----------------------------------------------------
        # OPPORTUNITY MATCHING
        # -----------------------------------------------------

        opportunity_matches = []

        for opportunity in opportunities:

            location_match = (
                opportunity.location.lower()
                == problem.location.lower()
            )

            if not location_match:
                continue

            reasons = [
                f"Available in {problem.location}",
                (
                    "Relevant to "
                    f"{problem.title.lower()}."
                ),
            ]

            opportunity_matches.append({

                "id": opportunity.id,

                "title": opportunity.title,

                "organization": opportunity.organization,

                "reason": (
                    "Location match + agricultural "
                    "context match."
                ),

                "reasons": reasons,

            })

        # -----------------------------------------------------
        # FINAL RESULT
        # -----------------------------------------------------

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