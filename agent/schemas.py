from pydantic import BaseModel

class WeatherResponse(BaseModel):
    city: str
    temperature: str
    description: str

class FetchResponse(BaseModel):
    url: str
    status_code: int
    content: str

class UserCreate(BaseModel):
    user_name:str

class UserOut(BaseModel):
    id:int
    user_name:str