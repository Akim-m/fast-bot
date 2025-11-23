from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from services.inventory_service import create_item, list_items, update_item, delete_item
from storage.db import get_db
from schemas import InventoryCreate, InventoryUpdate, InventoryOut

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=InventoryOut, status_code=status.HTTP_201_CREATED)
def create_item_route(item: InventoryCreate, db: Session = Depends(get_db)):
    """Create a new inventory item"""
    return create_item(db, item.item_name, item.quantity)

@router.get("/", response_model=list[InventoryOut])
def list_items_route(db: Session = Depends(get_db)):
    """List all inventory items"""
    return list_items(db)

@router.put("/{item_id}", response_model=InventoryOut)
def update_item_route(
    item_id: int = Path(..., gt=0, description="Item ID must be positive"),
    item: InventoryUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update an existing inventory item"""
    updated_item = update_item(db, item_id, item.item_name, item.quantity)
    if not updated_item:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_route(
    item_id: int = Path(..., gt=0, description="Item ID must be positive"),
    db: Session = Depends(get_db)
):
    """Delete an inventory item"""
    result = delete_item(db, item_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return None