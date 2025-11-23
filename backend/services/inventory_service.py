from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from storage.models import Inventory
from typing import Optional

def create_item(db: Session, item_name: str, quantity: int = 0) -> Inventory:
    """Create a new inventory item"""
    try:
        item = Inventory(item_name=item_name, quantity=quantity)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error creating item: {str(e)}")

def list_items(db: Session) -> list[Inventory]:
    """List all inventory items"""
    return db.query(Inventory).all()

def update_item(db: Session, item_id: int, item_name: str, quantity: int) -> Optional[Inventory]:
    """Update an inventory item"""
    try:
        item = db.query(Inventory).filter(Inventory.item_id == item_id).first()
        if item:
            item.item_name = item_name
            item.quantity = quantity
            db.commit()
            db.refresh(item)
        return item
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error updating item: {str(e)}")

def delete_item(db: Session, item_id: int) -> Optional[dict]:
    """Delete an inventory item"""
    try:
        item = db.query(Inventory).filter(Inventory.item_id == item_id).first()
        if item:
            db.delete(item)
            db.commit()
            return {"detail": "Item deleted"}
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error deleting item: {str(e)}")