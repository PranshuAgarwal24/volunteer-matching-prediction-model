from models import Volunteer, NGO, Match
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib
import os
import random

locations = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai"]
skills = ["teaching", "medical", "fundraising", "logistics", "counseling"]
MODEL_PATH = "best.pt"

def calculate_match_score(volunteer: Volunteer, ngo: NGO) -> float:
    location_score = 1.0 if volunteer.volunteer_location == ngo.ngo_location else 0.0
    skill_overlap = len(set(volunteer.volunteer_skills) & set(ngo.ngo_required_skills))
    skill_score = skill_overlap / max(len(ngo.ngo_required_skills), 1)
    availability_bonus = 0.05 if volunteer.volunteer_availability else 0.0
    return 0.7 * location_score + 0.3 * skill_score + availability_bonus

def generate_synthetic_data(n=1000):
    data = []
    for _ in range(n):
        v_loc = random.choice(locations)
        v_skills = random.sample(skills, k=random.randint(1, 3))
        v_avail = random.choice([True, False])
        n_loc = random.choice(locations)
        n_skills = random.sample(skills, k=random.randint(1, 3))
        score = calculate_match_score(
            Volunteer(
                volunteer_id="v",
                volunteer_location=v_loc,
                volunteer_skills=v_skills,
                volunteer_availability=v_avail
            ),
            NGO(
                ngo_id="n",
                ngo_location=n_loc,
                ngo_required_skills=n_skills
            )
        )
        data.append({
            "v_loc": v_loc,
            "v_avail": v_avail,
            "n_loc": n_loc,
            "v_skills": v_skills,
            "n_skills": n_skills,
            "score": score,
            "label": int(score >= 0.5)
        })
    return pd.DataFrame(data)

def train_model():
    df = generate_synthetic_data()
    df["skill_overlap"] = df.apply(lambda row: len(set(row["v_skills"]) & set(row["n_skills"])), axis=1)
    df["loc_match"] = (df["v_loc"] == df["n_loc"]).astype(int)
    df["avail"] = df["v_avail"].astype(int)
    X = df[["skill_overlap", "loc_match", "avail"]]
    y = df["label"]
    model = RandomForestClassifier()
    model.fit(X, y)
    save_model(model)
    return model, X.columns.tolist()

def save_model(model, filename=MODEL_PATH):
    joblib.dump(model, filename)
    print(f"✅ Model saved to {filename}")

_model = None

def load_model(path="best.pt"):
    global _model
    if _model is None:
        print(f"✅ Loading model from {path}")
        _model = joblib.load(path)
    return _model

def extract_features(volunteer: Volunteer, ngo: NGO):
    return {
        "skill_overlap": len(set(volunteer.volunteer_skills) & set(ngo.ngo_required_skills)),
        "loc_match": int(volunteer.volunteer_location == ngo.ngo_location),
        "avail": int(volunteer.volunteer_availability)
    }

def find_matches(volunteers, ngos, top_n=5, use_model=True):
    model = load_model() if use_model else None
    matches = []
    for volunteer in volunteers:
        scored = []
        for ngo in ngos:
            features = extract_features(volunteer, ngo)
            score = model.predict_proba([list(features.values())])[0][1] if model else calculate_match_score(volunteer, ngo)
            scored.append({
                "volunteer_id": volunteer.volunteer_id,
                "ngo_id": ngo.ngo_id,
                "match_score": score,
                "volunteer_location": volunteer.volunteer_location,
                "ngo_location": ngo.ngo_location,
                "volunteer_skills": volunteer.volunteer_skills,
                "ngo_required_skills": ngo.ngo_required_skills,
                "volunteer_availability": volunteer.volunteer_availability
            })
        top_matches = sorted(scored, key=lambda x: x["match_score"], reverse=True)[:top_n]
        matches.extend([Match(**m) for m in top_matches])
    return matches
