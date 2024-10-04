from fastapi import APIRouter, HTTPException
from typing import List
from models.item_model import items_db, find_item_by_id, ItemModel
from schemas.item_schema import ItemSchema
router = APIRouter()

# Get all items
@router.get("/items/", response_model=List[ItemSchema])
def get_items():
    return items_db

# Get a single item by ID
@router.get("/items/{item_id}", response_model=ItemSchema)
def get_item(item_id: int):
    item = find_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Create a new item
@router.post("/items/", response_model=ItemSchema)
def create_item(item: ItemSchema):
    # Check if item with the same ID already exists
    if find_item_by_id(item.id):
        raise HTTPException(status_code=400, detail="Item with this ID already exists.")
    
    new_item = ItemModel(id=item.id, name=item.name, description=item.description)
    items_db.append(new_item)
    return new_item

# Update an item by ID
@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item(item_id: int, updated_item: ItemSchema):
    item = find_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.name = updated_item.name
    item.description = updated_item.description
    return item

# Delete an item by ID
@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    global items_db
    items_db = [item for item in items_db if item.id != item_id]
    return {"message": "Item deleted"}
