from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user, list_users, update_user, delete_user
from storage.db import get_db
from schemas import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return create_user(db, user.user_name)

@router.get("/{user_id}", response_model=UserOut)
def get_user_route(
    user_id: int = Path(..., gt=0, description="User ID must be positive"),
    db: Session = Depends(get_db)
):
    """Get a specific user by ID"""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return user

@router.get("/", response_model=list[UserOut])
def list_users_route(db: Session = Depends(get_db)):
    """List all users"""
    return list_users(db)

@router.put("/{user_id}", response_model=UserOut)
def update_user_route(
    user_id: int = Path(..., gt=0, description="User ID must be positive"),
    user: UserUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update an existing user"""
    updated_user = update_user(db, user_id, user.user_name)
    if not updated_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
    user_id: int = Path(..., gt=0, description="User ID must be positive"),
    db: Session = Depends(get_db)
):
    """Delete a user"""
    result = delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return None