from fastapi import FastAPI
from app.routes import user_routes, inventory_routes, random_routes
from app.storage.db import initialize_database
from app.routes.weather_routes import router as weather_router

app = FastAPI(title="Full CRUD + Weather API")

initialize_database()

app.include_router(user_routes.router)
app.include_router(inventory_routes.router)
app.include_router(random_routes.router)
app.include_router(weather_router)

@app.get("/")
def home():
    return {"message": "Welcome to the API!"}
