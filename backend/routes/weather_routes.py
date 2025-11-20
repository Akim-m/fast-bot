from fastapi import APIRouter
from app.services.weather_service import get_weather

router = APIRouter()

@router.get("/weather/city/{city}")
async def weather_by_city(city: str):
    return get_weather(city)
