from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import scoring

app = FastAPI()

# allow both localhost and 127.0.0.1 from Vite
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"status": "connected"}

@app.get("/factors")
async def get_factors():
    # serve the same factors.json data
    return {"factors": scoring.factors}

@app.post("/score")
async def score_endpoint(data: dict):
    return scoring.calculate_score(data)

@app.post("/recommend")
async def recommend_endpoint(data: dict):
    return scoring.recommend_next_level(data)