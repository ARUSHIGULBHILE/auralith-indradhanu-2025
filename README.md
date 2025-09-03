# Digital Twin — Hackathon Starter

A minimal, team-friendly repository skeleton to build a **Digital Twin** prototype fast.  
Includes a Python FastAPI backend, folders for a web frontend, data, docs, and basic CI.

## Quick Start

### 1) Create & activate a Python virtual environment
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2) Install backend dependencies
```bash
pip install -r backend/requirements.txt
```

### 3) Run the API
```bash
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

Open: http://localhost:8000/docs

### 4) Frontend (you can scaffold later)
Inside `frontend/`, run any framework you like (e.g., Vite + React):
```bash
# Example
npm create vite@latest dashboard -- --template react
cd dashboard
npm install
npm run dev
```

## What’s inside
```
backend/          # FastAPI app (ingest, state, websocket)
frontend/         # Your web UI (scaffold React/Vite or any framework)
data/             # Sample/collected datasets and logs
docs/             # Diagrams, notes, API docs
.github/workflows # CI placeholder
```

## API Sketch
- `GET /health` — service check
- `POST /ingest` — send sensor/event payloads `{ device_id, ts, metrics }`
- `GET /state/{device_id}` — fetch last known state for a device
- `WebSocket /ws` — realtime updates to the dashboard

## Team Workflow
1. Branches: `main` (stable), `dev` (active), `feature/*` (per task)
2. Create Issues and link to Pull Requests
3. One teammate reviews every PR before merging to `dev` or `main`

## License
MIT — see `LICENSE`.
