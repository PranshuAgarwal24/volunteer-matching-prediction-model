import requests

url = "http://127.0.0.1:8000/match/"
data = {
    "volunteers": [
        {
            "volunteer_id": "vol1",
            "volunteer_location": "Mumbai",
            "volunteer_skills": ["teaching", "counseling"],
            "volunteer_availability": True
        }
    ],
    "ngos": [
        {
            "ngo_id": "ngo1",
            "ngo_location": "Mumbai",
            "ngo_required_skills": ["teaching"]
        },
        {
            "ngo_id": "ngo2",
            "ngo_location": "Delhi",
            "ngo_required_skills": ["counseling"]
        },
        {
            "ngo_id": "ngo3",
            "ngo_location": "Mumbai",
            "ngo_required_skills": ["logistics"]
        }
    ]
}

response = requests.post(url, json=data)
print(response.json())
