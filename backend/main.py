from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data.demo_data import people, problems, opportunities
from backend.matching_engine import find_matches
from backend.query_engine import query_sang
from backend.three_three_three import (
    route_333,
    start_333_session,
    continue_333_session,
)

from backend.voice_pipeline import build_voice_pipeline


app = FastAPI(
    title="SANG",
    version="0.1.0",
    description="Connective intelligence for people, problems, resources and opportunities."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ThreeThreeThreeRequest(BaseModel):
    message: str


class ThreeThreeThreeFollowUpRequest(BaseModel):
    session_id: str
    message: str


active_333_sessions = {}


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


@app.post("/333")
def three_three_three(request: ThreeThreeThreeRequest):
    session = start_333_session(request.message)

    active_333_sessions[session["session_id"]] = session

    return session


@app.post("/333/voice")
def three_three_three_voice(request: ThreeThreeThreeRequest):
    session = start_333_session(request.message)

    active_333_sessions[session["session_id"]] = session

    route = session.get("route", "UNKNOWN")

    return {
        **session,
        "voice_pipeline": build_voice_pipeline(
            request.message,
            route,
            session,
        ),
    }


@app.post("/333/{session_id}")
def continue_three_three_three(
    session_id: str,
    request: ThreeThreeThreeRequest,
):
    session = active_333_sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="333 session not found"
        )

    updated_session = continue_333_session(
        session,
        request.message,
    )

    active_333_sessions[session_id] = updated_session

    return updated_session