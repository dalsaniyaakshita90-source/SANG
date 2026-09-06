import re


def parse_query(query: str):
    query_lower = query.lower()

    skills = []
    categories = []
    location = None

    known_skills = [
        "python",
        "data analysis",
        "machine learning",
        "textile design",
        "sustainability",
        "graphic design",
        "teaching",
        "gujarati",
        "community outreach",
    ]

    known_categories = [
        "agriculture",
        "sustainability",
        "education",
        "rural development",
        "ai",
    ]

    known_locations = [
        "ahmedabad",
        "surat",
        "rajkot",
        "gujarat",
    ]

    for skill in known_skills:
        if skill in query_lower:
            skills.append(skill)

    for category in known_categories:
        if category in query_lower:
            categories.append(category)

    for city in known_locations:
        if city in query_lower:
            location = city.title()

    return {
        "original_query": query,
        "skills": skills,
        "categories": categories,
        "location": location,
    }
