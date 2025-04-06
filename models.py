from pydantic import BaseModel
from typing import List

class Volunteer(BaseModel):
    volunteer_id: str
    volunteer_location: str
    volunteer_skills: List[str]
    volunteer_availability: bool  # True for full-time, False for part-time

class NGO(BaseModel):
    ngo_id: str
    ngo_location: str
    ngo_required_skills: List[str]

class MatchRequest(BaseModel):
    volunteers: List[Volunteer]
    ngos: List[NGO]

class Match(BaseModel):
    volunteer_id: str
    ngo_id: str
    match_score: float
    volunteer_location: str
    ngo_location: str
    volunteer_skills: List[str]
    ngo_required_skills: List[str]
    volunteer_availability: bool

class MatchResponse(BaseModel):
    matches: List[Match]
