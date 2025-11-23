from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from storage.models import User
from typing import Optional

def create_user(db: Session, user_name: str) -> User:
    """Create a new user"""
    try:
        user = User(user_name=user_name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error creating user: {str(e)}")

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID"""
    return db.query(User).filter(User.user_id == user_id).first()

def list_users(db: Session) -> list[User]:
    """List all users"""
    return db.query(User).all()

def update_user(db: Session, user_id: int, user_name: str) -> Optional[User]:
    """Update a user's information"""
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.user_name = user_name
            db.commit()
            db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error updating user: {str(e)}")

def delete_user(db: Session, user_id: int) -> Optional[dict]:
    """Delete a user"""
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return {"detail": "User deleted"}
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error deleting user: {str(e)}")