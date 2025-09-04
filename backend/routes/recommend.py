from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def recommend():
    # Placeholder response: top 3 crops with simple scores
    return {
        "top_crops": [
            {"crop": "Wheat", "score": 87, "reason": "Suitable soil & high market price"},
            {"crop": "Maize", "score": 78, "reason": "Moderate water requirement"},
            {"crop": "Soybean", "score": 70, "reason": "Good profit margin"}
        ]
    }
