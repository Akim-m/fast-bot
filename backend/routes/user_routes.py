from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.user_service import create_user, get_user, list_users, update_user, delete_user
from app.storage.db import get_db
from app.schemas import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.user_name)

@router.get("/{user_id}", response_model=UserOut)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@router.get("/", response_model=list[UserOut])
def list_users_route(db: Session = Depends(get_db)):
    return list_users(db)

@router.put("/{user_id}", response_model=UserOut)
def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user.user_name)

@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
