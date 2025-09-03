from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

app = FastAPI(title="Digital Twin API", version="0.1.0")

# In-memory "digital twin" state store (replace with DB in production)
TWIN_STATE: Dict[str, Dict[str, Any]] = {}
ACTIVE_CONNECTIONS: set[WebSocket] = set()

class IngestPayload(BaseModel):
    device_id: str
    ts: Optional[datetime] = None
    metrics: Dict[str, float] = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(payload: IngestPayload):
    ts = payload.ts.isoformat() if payload.ts else datetime.utcnow().isoformat()
    state = {"device_id": payload.device_id, "ts": ts, "metrics": payload.metrics}
    TWIN_STATE[payload.device_id] = state
    # Broadcast to any connected dashboards
    dead = []
    for ws in list(ACTIVE_CONNECTIONS):
        try:
            import json
            ws_payload = {"type": "update", "data": state}
            # Send text so a basic JS client can parse it
            ws.send_text(json.dumps(ws_payload))
        except Exception:
            dead.append(ws)
    for ws in dead:
        try:
            ACTIVE_CONNECTIONS.remove(ws)
        except KeyError:
            pass
    return {"ok": True, "stored": state}

@app.get("/state/{device_id}")
def get_state(device_id: str):
    return TWIN_STATE.get(device_id, {"device_id": device_id, "message": "no state yet"})

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    ACTIVE_CONNECTIONS.add(websocket)
    try:
        while True:
            # We don't expect messages from client; just keep alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        try:
            ACTIVE_CONNECTIONS.remove(websocket)
        except KeyError:
            pass
