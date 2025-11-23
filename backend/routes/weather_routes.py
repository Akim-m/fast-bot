from fastapi import APIRouter, Path
from services.weather_service import get_weather
from schemas import WeatherOut

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/city/{city}", response_model=WeatherOut)
async def weather_by_city(
    city: str = Path(..., min_length=1, max_length=100, description="City name to get weather for")
):
    """
    Get current weather information for a specified city
    """
    return get_weather(city)