from fastapi import FastAPI
from backend.routes import iot, recommend, simulate

app = FastAPI(title="Digital Twin Farm - Backend")

app.include_router(iot.router, prefix="/iot")
app.include_router(recommend.router, prefix="/recommend")
app.include_router(simulate.router, prefix="/simulate")

@app.get("/")
def root():
    return {"message": "Digital Twin Farm Backend Running"}
