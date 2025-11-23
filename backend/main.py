from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_routes, inventory_routes, random_routes
from routes.health_routes import router as health_router
from routes.db_router import router as db_router
from routes.backup_routes import router as backup_router
from storage.db import initialize_database
from routes.weather_routes import router as weather_router
from services.backup_scheduler import lifespan_with_backup

app = FastAPI(
    title="Full CRUD + Weather API with Auto-Backup",
    description="FastAPI application with automatic database backups every 5 minutes",
    version="1.0.2",
    lifespan=lifespan_with_backup
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()

app.include_router(health_router)
app.include_router(user_routes.router)
app.include_router(inventory_routes.router)
app.include_router(random_routes.router)
app.include_router(weather_router)
app.include_router(db_router)
app.include_router(backup_router)

@app.get("/")
def home():
    return {
        "message": "API with Auto-Backup",
        "version": "1.0.2",
        "backup_interval": "5 minutes",
        "endpoints": {
            "health": "/health",
            "users": "/users",
            "inventory": "/inventory",
            "weather": "/weather/city/{city}",
            "random": "/random",
            "database": "/db",
            "backup": "/backup",
            "docs": "/docs"
        }
    }