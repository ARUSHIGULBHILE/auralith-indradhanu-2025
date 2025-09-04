from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SimInput(BaseModel):
    rainfall: float
    temperature: float
    crop: str

@router.post("/")
def simulate(input: SimInput):
    # Simple placeholder logic for yield/profit/eco_score calculation
    base_yield = 100.0
    yield_adj = base_yield * (1 + (input.rainfall - 50)/100) * (1 - abs(input.temperature-25)/100)
    profit = yield_adj * 200  # dummy price
    eco_score = max(0, 100 - (abs(input.rainfall-50)/1.5))
    return {"estimated_yield": round(yield_adj,2), "estimated_profit": round(profit,2), "eco_score": round(eco_score,2)}
