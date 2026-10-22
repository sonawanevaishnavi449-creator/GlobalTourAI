
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.recommendation_engine import recommend_destinations

app = FastAPI(
    title="GlobalTourAI API",
    description="API for personalized Indian travel recommendations",
    version="1.0.0",
)


class RecommendationRequest(BaseModel):
    query: str = Field(min_length=1)
    budget: float = Field(gt=0)
    days: int = Field(gt=0)
    season: Literal["Winter", "Summer", "Monsoon"]
    traveler: Literal[
        "Solo",
        "Couple",
        "Friends",
        "Family_with_kids",
        "Family_with_elderly",
    ]


@app.get("/")
def home():
    return {
        "message": "Welcome to GlobalTourAI API!",
        "status": "running",
        "docs": "/docs",
    }


@app.post("/recommend")
def get_recommendations(request: RecommendationRequest):
    results = recommend_destinations(
        query=request.query.strip(),
        budget=request.budget,
        days=request.days,
        season=request.season,
        traveler=request.traveler,
    )

    return {
        "success": True,
        "count": len(results),
        "recommendations": results,
    }
