from fastapi import APIRouter, HTTPException
from typing import List
from models.item_model import items_db, find_item_by_id, ItemModel, link_extraction
from schemas.item_schema import Item, LinkExtractionRequest

router = APIRouter()


# # Get all items
# @router.get("/items/", response_model=None)
# def get_items():
#     return items_db


# # Get a single item by ID
# @router.get("/items/{item_id}", response_model=None)
# def get_item(item_id: int):
#     item = find_item_by_id(item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item


# # Create a new item
# @router.post("/items/", response_model=None)
# def create_item(item: int):
#     # Check if item with the same ID already exists
#     if find_item_by_id(item.id):
#         raise HTTPException(status_code=400, detail="Item with this ID already exists.")

#     new_item = ItemModel(id=item.id, name=item.name, description=item.description)
#     items_db.append(new_item)
#     return new_item


# # Update an item by ID
# @router.put("/items/{item_id}", response_model=None)
# def update_item(item_id: int, updated_item: int):
#     item = find_item_by_id(item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")

#     item.name = updated_item.name
#     item.description = updated_item.description
#     return item


# # Delete an item by ID
# @router.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     global items_db
#     items_db = [item for item in items_db if item.id != item_id]
#     return {"message": "Item deleted"}


# Create a new item
@router.post("/items/link_extraction", response_model=None)
async def get_link_extraction_item(link_extraction_request: LinkExtractionRequest):
    """
    View that handles the incoming POST request for link extraction.
    It passes the request data to the controller and returns the response.
    """
    # Call the controller to get the items
    items = await link_extraction(
        name=link_extraction_request.name,
        start_year=link_extraction_request.start_year,
        end_year=link_extraction_request.end_year,
        number_of_urls=link_extraction_request.number_of_urls,
    )

    if not items:
        raise HTTPException(status_code=404, detail="Items not found")

    return items
