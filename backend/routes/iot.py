from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SensorPayload(BaseModel):
    device_id: str
    soil_moisture: float
    temperature: float
    humidity: float
    timestamp: str

@router.post("/ingest")
def ingest_sensor(payload: SensorPayload):
    # Placeholder: store payload to DB or file
    return {"status": "ok", "received": payload.dict()}
