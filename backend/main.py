from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scoring import calculate_score, recommend_next_level

app = FastAPI()

# Allow requests from your Svelte dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"status": "connected"}

@app.post("/score")
async def score(data: dict):
    return calculate_score(data)

@app.post("/recommend")
async def recommend_endpoint(data:dict): 
    return recommend_next_level(data)