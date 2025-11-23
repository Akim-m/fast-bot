from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional

# User Schemas
class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=100, description="Username must be 1-100 characters")
    
    @field_validator('user_name')
    @classmethod
    def validate_user_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Username cannot be empty or just whitespace')
        return v.strip()

class UserUpdate(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=100)
    
    @field_validator('user_name')
    @classmethod
    def validate_user_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Username cannot be empty or just whitespace')
        return v.strip()

class UserOut(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID must be positive")
    user_name: str
    
    model_config = ConfigDict(from_attributes=True)

# Inventory Schemas
class InventoryCreate(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=200, description="Item name must be 1-200 characters")
    quantity: int = Field(default=0, ge=0, description="Quantity must be non-negative")
    
    @field_validator('item_name')
    @classmethod
    def validate_item_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Item name cannot be empty or just whitespace')
        return v.strip()

class InventoryUpdate(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., ge=0, description="Quantity must be non-negative")
    
    @field_validator('item_name')
    @classmethod
    def validate_item_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Item name cannot be empty or just whitespace')
        return v.strip()

class InventoryOut(BaseModel):
    item_id: int = Field(..., gt=0, description="Item ID must be positive")
    item_name: str
    quantity: int = Field(..., ge=0)
    
    model_config = ConfigDict(from_attributes=True)

# Weather Schemas
class WeatherOut(BaseModel):
    city: str = Field(..., min_length=1, description="City name is required")
    temperature: float = Field(..., description="Temperature in Celsius")
    description: str = Field(..., min_length=1, description="Weather description")

# Random Number Schema
class RandomNumberOut(BaseModel):
    number: int = Field(..., ge=0, le=100, description="Random number between 0 and 100")

# Health Check Schema
class HealthCheckOut(BaseModel):
    status: str = Field(..., description="API health status")
    database: str = Field(..., description="Database connection status")
    timestamp: str = Field(..., description="Health check timestamp")