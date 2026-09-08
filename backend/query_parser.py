import re


def contains_term(query, term):
    pattern = r"\b" + re.escape(term.lower()) + r"\b"
    return re.search(pattern, query.lower()) is not None


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
        if contains_term(query_lower, skill):
            skills.append(skill)

    for category in known_categories:
        if contains_term(query_lower, category):
            categories.append(category)

    for city in known_locations:
        if contains_term(query_lower, city):
            location = city.title()

    return {
        "original_query": query,
        "skills": skills,
        "categories": categories,
        "location": location,
    }