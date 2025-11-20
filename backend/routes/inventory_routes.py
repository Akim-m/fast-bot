from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.inventory_service import create_item, list_items, update_item, delete_item
from app.storage.db import get_db
from app.schemas import InventoryCreate, InventoryUpdate, InventoryOut

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=InventoryOut)
def create_item_route(item: InventoryCreate, db: Session = Depends(get_db)):
    return create_item(db, item.item_name, item.quantity)

@router.get("/", response_model=list[InventoryOut])
def list_items_route(db: Session = Depends(get_db)):
    return list_items(db)

@router.put("/{item_id}", response_model=InventoryOut)
def update_item_route(item_id: int, item: InventoryUpdate, db: Session = Depends(get_db)):
    return update_item(db, item_id, item.item_name, item.quantity)

@router.delete("/{item_id}")
def delete_item_route(item_id: int, db: Session = Depends(get_db)):
    return delete_item(db, item_id)
