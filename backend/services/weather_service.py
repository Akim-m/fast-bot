import requests
from fastapi import HTTPException
from schemas import WeatherOut

def get_weather(city: str) -> WeatherOut:
    """
    Fetch weather data for a given city from wttr.in API
    """
    if not city or not city.strip():
        raise HTTPException(status_code=400, detail="City name cannot be empty")
    
    city = city.strip()
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'current_condition' not in data or not data['current_condition']:
            raise HTTPException(status_code=404, detail=f"Weather data not found for city: {city}")
        
        current_condition = data['current_condition'][0]
        temp_c = float(current_condition['temp_C'])
        desc = current_condition['weatherDesc'][0]['value']
        
        return WeatherOut(
            city=city,
            temperature=temp_c,
            description=desc
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Weather service unavailable: {str(e)}")
    except (KeyError, ValueError, IndexError) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing weather data: {str(e)}")