import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("agritwin.api_client")

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000", timeout_seconds: int = 5):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout_seconds

    def _get(self, path: str) -> Optional[Dict[str, Any]]:
        import requests
        url = f"{self.base_url}{path}"
        try:
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.warning(f"GET {url} failed: {e}")
            return None

    def _post(self, path: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        import requests
        url = f"{self.base_url}{path}"
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.warning(f"POST {url} failed: {e}")
            return None

    def get_latest_sensors(self) -> List[Dict[str, Any]]:
        data = self._get("/iot/")
        if not data:
            return self._mock_sensors()
        return data.get("sensors", [])

    def get_recommendations(self) -> List[Dict[str, Any]]:
        data = self._get("/recommend/")
        if not data:
            return self._mock_recommendations()
        return data.get("top_crops", [])

    def simulate(self, rainfall: float, temperature: float, crop: str) -> Dict[str, Any]:
        payload = {"rainfall": rainfall, "temperature": temperature, "crop": crop}
        data = self._post("/simulate/", payload)
        if not data:
            return self._mock_simulation(rainfall, temperature, crop)
        return data

    # --- Mock functions ---
    def _mock_sensors(self):
        from time import strftime
        return [
            {
                "device_id": "sim-01",
                "soil_moisture": 35.2,
                "temperature": 27.1,
                "humidity": 62.3,
                "timestamp": strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

    def _mock_recommendations(self):
        return [
            {"crop": "Wheat", "score": 87, "reason": "Suitable soil & strong market price"},
            {"crop": "Maize", "score": 78, "reason": "Moderate water requirement"},
            {"crop": "Soybean", "score": 70, "reason": "High margin & low input"}
        ]

    def _mock_simulation(self, rainfall, temperature, crop):
        base_yield = 100.0
        yield_adj = base_yield * (1 + (rainfall - 50)/100) * (1 - abs(temperature - 25)/100)
        profit = yield_adj * 200
        eco = max(0.0, 100.0 - abs(rainfall - 50)/1.5)
        return {"estimated_yield": round(yield_adj,2), "estimated_profit": round(profit,2), "eco_score": round(eco,2)}
