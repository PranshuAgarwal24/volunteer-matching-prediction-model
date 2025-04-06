from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import MatchRequest, MatchResponse
from matching import find_matches, locations, skills, train_model

app = FastAPI(
    title="Volunteer-NGO Matching API",
    description="API for matching volunteers with NGOs based on location and skills"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, replace * with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/match/", response_model=MatchResponse)
async def match_volunteers_with_ngos(request: MatchRequest, top_n: int = 5, use_model: bool = True):
    for volunteer in request.volunteers:
        if volunteer.volunteer_location not in locations:
            raise HTTPException(status_code=400, detail=f"Invalid location: {volunteer.volunteer_location}")
        for skill in volunteer.volunteer_skills:
            if skill not in skills:
                raise HTTPException(status_code=400, detail=f"Invalid skill: {skill}")
    for ngo in request.ngos:
        if ngo.ngo_location not in locations:
            raise HTTPException(status_code=400, detail=f"Invalid location: {ngo.ngo_location}")
        for skill in ngo.ngo_required_skills:
            if skill not in skills:
                raise HTTPException(status_code=400, detail=f"Invalid skill: {skill}")
    matches = find_matches(request.volunteers, request.ngos, top_n, use_model)
    return MatchResponse(matches=matches)

@app.post("/train/")
async def train_matching_model():
    model, feature_cols = train_model()
    return {"message": "Model trained successfully", "feature_count": len(feature_cols)}

@app.get("/")
async def root():
    return {
        "message": "Volunteer-NGO Matching API",
        "version": "1.0.0",
        "locations": locations,
        "skills": skills
    }

@app.get("/locations/")
async def get_locations():
    return {"locations": locations}

@app.get("/skills/")
async def get_skills():
    return {"skills": skills}
