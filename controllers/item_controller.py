from fastapi import APIRouter, HTTPException
from typing import List
from models.item_model import items_db, ItemModel, link_extraction
from schemas.item_schema import Item, LinkExtractionRequest

router = APIRouter()

# Create a link_extraction end-point
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
        domain=link_extraction_request.domain,
    )

    if not items:
        raise HTTPException(status_code=404, detail="Items not found")

    return items
