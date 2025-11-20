from sqlalchemy.orm import Session
from app.storage.models import User

def create_user(db: Session, user_name: str):
    user = User(user_name=user_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def list_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, user_name: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.user_name = user_name
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return {"detail": "User deleted"}
