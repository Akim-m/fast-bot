from fastapi import APIRouter
from app.services.random_service import generate_random_number
from app.schemas import RandomNumberOut

router = APIRouter(prefix="/random", tags=["Random"])

@router.get("/", response_model=RandomNumberOut)
def get_random_number_route():
    return {"number": generate_random_number()}
