import requests
from pydantic import BaseModel

class WeatherResponse(BaseModel):
    city: str
    temperature: str
    description: str

def get_weather(city: str) -> WeatherResponse:

    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    data = response.json()

    current_condition = data['current_condition'][0]
    temp_c = current_condition['temp_C']
    desc = current_condition['weatherDesc'][0]['value']

    return WeatherResponse(
        city=city,
        temperature=f"{temp_c} °C",
        description=desc
    )
