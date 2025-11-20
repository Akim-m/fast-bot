from sqlalchemy.orm import Session
from app.storage.models import Inventory

def create_item(db: Session, item_name: str, quantity: int = 0):
    item = Inventory(item_name=item_name, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_items(db: Session):
    return db.query(Inventory).all()

def update_item(db: Session, item_id: int, item_name: str, quantity: int):
    item = db.query(Inventory).filter(Inventory.item_id == item_id).first()
    if item:
        item.item_name = item_name
        item.quantity = quantity
        db.commit()
        db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = db.query(Inventory).filter(Inventory.item_id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return {"detail": "Item deleted"}
