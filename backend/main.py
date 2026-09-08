from fastapi import FastAPI, HTTPException

from data.demo_data import people, problems, opportunities
from backend.matching_engine import find_matches
from backend.query_engine import query_sang


app = FastAPI(
    title="SANG",
    version="0.1.0",
    description="Connective intelligence for people, problems, resources and opportunities."
)


@app.get("/")
def root():
    return {
        "name": "SANG",
        "version": "0.1.0",
        "status": "alive"
    }


@app.get("/people")
def get_people():
    return people


@app.get("/problems")
def get_problems():
    return problems


@app.get("/opportunities")
def get_opportunities():
    return opportunities


@app.get("/match/{person_id}")
def get_matches(person_id: str):
    person = next(
        (person for person in people if person.id == person_id),
        None
    )

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    return {
        "person": person,
        "matches": find_matches(
            person,
            problems,
            opportunities
        )
    }



@app.get("/query")
def query(query: str):
    return query_sang(query)
from data.resources import resources


@app.get("/resources")
def get_resources():
    return resources
from backend.resource_matching import find_resource_matches

@app.get("/problems/{problem_id}/resources")
def get_problem_resources(problem_id: str):
    problem = next(
        (problem for problem in problems if problem.id == problem_id),
        None
    )

    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    return {
        "problem": problem,
        "resources": find_resource_matches(problem)
    }


from backend.agriculture_engine import get_agriculture_data

@app.get("/agriculture")
def agriculture():
    return get_agriculture_data()