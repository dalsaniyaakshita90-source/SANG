from pydantic import BaseModel
from typing import List


class Person(BaseModel):
    id: str
    name: str
    location: str
    skills: List[str]
    interests: List[str]
    availability: str
    accessibility_needs: List[str] = []


class Problem(BaseModel):
    id: str
    title: str
    description: str
    organization: str
    location: str
    required_skills: List[str]
    category: str


class Opportunity(BaseModel):
    id: str
    title: str
    description: str
    organization: str
    location: str
    required_skills: List[str]
    eligibility: List[str]
    category: str


class Resource(BaseModel):
    id: str
    name: str
    resource_type: str
    description: str
    location: str


class Match(BaseModel):
    target_id: str
    target_type: str
    score: float
    reasons: List[str]
