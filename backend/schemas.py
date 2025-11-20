from pydantic import BaseModel

class UserCreate(BaseModel):
    user_name: str

class UserUpdate(BaseModel):
    user_name: str

class UserOut(BaseModel):
    user_id: int
    user_name: str

    class Config:
        orm_mode = True

class InventoryCreate(BaseModel):
    item_name: str
    quantity: int = 0

class InventoryUpdate(BaseModel):
    item_name: str
    quantity: int

class InventoryOut(BaseModel):
    item_id: int
    item_name: str
    quantity: int

    class Config:
        orm_mode = True

class WeatherOut(BaseModel):
    city: str
    temperature: float
    description: str

class RandomNumberOut(BaseModel):
    number: int
