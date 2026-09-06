from .models import Person, Problem, Opportunity, Match
from .matching import match_person_to_target


def find_matches(person, problems, opportunities):
    matches = []

    for problem in problems:
        match = match_person_to_target(person, problem)
        matches.append(match)

    for opportunity in opportunities:
        match = match_person_to_target(person, opportunity)
        matches.append(match)

    matches.sort(key=lambda match: match.score, reverse=True)

    return matches
